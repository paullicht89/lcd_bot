#!/bin/bash
set -euo pipefail

SERVER="${LCD_BOT_DEPLOY_SERVER:-lcd-do-hris}"
PROD_APP_DIR="${LCD_BOT_PROD_APP_DIR:-/srv/lcd_bot}"
STAGING_APP_DIR="${LCD_BOT_STAGING_APP_DIR:-/srv/lcd_bot-staging}"
PROD_SERVICES=("${LCD_BOT_PROD_SERVICE:-lcd_bot}")
STAGING_SERVICES=("${LCD_BOT_STAGING_SERVICE:-lcd_bot-staging}")

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_STATE_DIR="$SCRIPT_DIR/.local"
WORKTREE_DIR="$LOCAL_STATE_DIR/production_worktree"
TEMP_BRANCH="deploy-production-temp"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
KEEP_WORKTREE=0
DEPLOY_TARGET=""
DEPLOY_BRANCH=""
APP_DIR=""
REMOTE_PATH=""
ACTIVE_SERVICES=()

remove_or_archive_worktree_path() {
    if [[ ! -d "$WORKTREE_DIR" ]]; then
        return
    fi

    local worktree_top=""
    worktree_top="$(git -C "$WORKTREE_DIR" rev-parse --show-toplevel 2>/dev/null || true)"
    local normalized_top=""
    local normalized_worktree=""
    if [[ -n "$worktree_top" ]]; then
        normalized_top="$(cd "$worktree_top" && pwd -P)"
    fi
    normalized_worktree="$(cd "$WORKTREE_DIR" && pwd -P)"

    if [[ -n "$normalized_top" && "$normalized_top" == "$normalized_worktree" ]]; then
        git -C "$REPO_ROOT" worktree remove --force "$WORKTREE_DIR"
        return
    fi

    local stale_path="${WORKTREE_DIR}.stale.$(date +%Y%m%d%H%M%S)"
    echo "Found stale production worktree folder that Git no longer tracks."
    echo "Moving it aside to: $stale_path"
    mv "$WORKTREE_DIR" "$stale_path"
}

cleanup() {
    if [[ "$KEEP_WORKTREE" -eq 1 ]]; then
        return
    fi

    remove_or_archive_worktree_path >/dev/null 2>&1 || true
    if git -C "$REPO_ROOT" show-ref --verify --quiet "refs/heads/$TEMP_BRANCH"; then
        git -C "$REPO_ROOT" branch -D "$TEMP_BRANCH" >/dev/null 2>&1 || true
    fi
}

trap cleanup EXIT

ensure_git_repo() {
    git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
        echo "Not inside a Git repository."
        exit 1
    }
}

fetch_branches() {
    echo "Fetching latest branch state from origin..."
    git -C "$REPO_ROOT" fetch origin main
    if git -C "$REPO_ROOT" fetch origin production >/dev/null 2>&1; then
        :
    else
        echo
        echo "origin/production does not exist yet."
        echo "Create it once before using production promotion:"
        echo "  git checkout main"
        echo "  git pull origin main"
        echo "  git checkout -b production"
        echo "  git push -u origin production"
        echo "  git checkout main"
        echo
    fi
}

prompt_for_target() {
    local selection

    echo "Choose deployment target:"
    echo "  1) staging  ($STAGING_APP_DIR, origin/main)"
    echo "  2) production ($PROD_APP_DIR, origin/production)"
    echo "  q) quit"
    read -rp "Select target: " selection

    case "$selection" in
        1|s|S|staging)
            DEPLOY_TARGET="staging"
            DEPLOY_BRANCH="main"
            APP_DIR="$STAGING_APP_DIR"
            REMOTE_PATH="$STAGING_APP_DIR"
            ACTIVE_SERVICES=("${STAGING_SERVICES[@]}")
            ;;
        2|p|P|prod|production)
            DEPLOY_TARGET="production"
            DEPLOY_BRANCH="production"
            APP_DIR="$PROD_APP_DIR"
            REMOTE_PATH="$PROD_APP_DIR"
            ACTIVE_SERVICES=("${PROD_SERVICES[@]}")
            ;;
        q|Q)
            echo "Deployment cancelled."
            exit 0
            ;;
        *)
            echo "Invalid target: $selection"
            exit 1
            ;;
    esac

    echo
    echo "Target: $DEPLOY_TARGET"
    echo "Server: $SERVER"
    echo "Remote path: $APP_DIR"
    echo "Branch: origin/$DEPLOY_BRANCH"
    echo
}

list_promotable_commits() {
    if ! git -C "$REPO_ROOT" show-ref --verify --quiet refs/remotes/origin/production; then
        echo "origin/production is missing. Run the one-time production branch setup first."
        exit 1
    fi
    mapfile -t AVAILABLE_COMMITS < <(git -C "$REPO_ROOT" log --reverse --oneline origin/production..main)
}

prompt_for_commit_selection() {
    local selection
    local -A seen=()

    if [[ ${#AVAILABLE_COMMITS[@]} -eq 0 ]]; then
        echo "No commits in main are waiting to be promoted to production."
        SELECTED_COMMITS=()
        SKIP_PROMOTION=1
        return
    fi

    echo "Commits available to promote from main to production:"
    for i in "${!AVAILABLE_COMMITS[@]}"; do
        printf "  %2d) %s\n" "$((i + 1))" "${AVAILABLE_COMMITS[$i]}"
    done
    echo
    echo "Choose commits to deploy:"
    echo "  a = all listed commits"
    echo "  s = skip commit promotion and sync/restart from current production"
    echo "  q = quit without deploying"
    read -rp "Enter numbers separated by spaces (oldest to newest recommended): " selection

    if [[ "$selection" == "q" || "$selection" == "Q" ]]; then
        echo "Deployment cancelled."
        exit 0
    fi

    if [[ "$selection" == "s" || "$selection" == "S" ]]; then
        SELECTED_COMMITS=()
        SKIP_PROMOTION=1
        return
    fi

    SELECTED_COMMITS=()
    if [[ "$selection" == "a" || "$selection" == "A" ]]; then
        for line in "${AVAILABLE_COMMITS[@]}"; do
            SELECTED_COMMITS+=("${line%% *}")
        done
        return
    fi

    for entry in $selection; do
        if [[ ! "$entry" =~ ^[0-9]+$ ]]; then
            echo "Invalid selection: $entry"
            exit 1
        fi

        local idx=$((entry - 1))
        if (( idx < 0 || idx >= ${#AVAILABLE_COMMITS[@]} )); then
            echo "Out-of-range selection: $entry"
            exit 1
        fi

        local commit_hash="${AVAILABLE_COMMITS[$idx]%% *}"
        if [[ -n "${seen[$commit_hash]:-}" ]]; then
            continue
        fi
        seen[$commit_hash]=1
        SELECTED_COMMITS+=("$commit_hash")
    done

    if [[ ${#SELECTED_COMMITS[@]} -eq 0 ]]; then
        echo "No commits selected."
        exit 0
    fi
}

prepare_production_worktree() {
    mkdir -p "$LOCAL_STATE_DIR"

    remove_or_archive_worktree_path

    if git -C "$REPO_ROOT" show-ref --verify --quiet "refs/heads/$TEMP_BRANCH"; then
        git -C "$REPO_ROOT" branch -D "$TEMP_BRANCH"
    fi

    git -C "$REPO_ROOT" branch "$TEMP_BRANCH" origin/production
    git -C "$REPO_ROOT" worktree add "$WORKTREE_DIR" "$TEMP_BRANCH"
}

promote_commits_to_production() {
    echo "Cherry-picking selected commits onto production..."

    for commit_hash in "${SELECTED_COMMITS[@]}"; do
        if ! git -C "$WORKTREE_DIR" cherry-pick "$commit_hash"; then
            if git -C "$WORKTREE_DIR" diff --quiet && git -C "$WORKTREE_DIR" diff --cached --quiet; then
                echo "Cherry-pick for $commit_hash was empty; skipping because production already contains those changes."
                git -C "$WORKTREE_DIR" cherry-pick --skip
                continue
            fi
            KEEP_WORKTREE=1
            echo
            echo "Cherry-pick failed for commit $commit_hash."
            echo "Resolve conflicts in: $WORKTREE_DIR"
            echo "Then run: git -C '$WORKTREE_DIR' cherry-pick --continue"
            echo "Or abort with: git -C '$WORKTREE_DIR' cherry-pick --abort"
            echo "After resolving, push production manually."
            exit 1
        fi
    done
}
push_production_branch() {
    echo "Pushing updated production branch to GitHub..."
    git -C "$WORKTREE_DIR" push origin HEAD:production
    git -C "$REPO_ROOT" fetch origin production
    git -C "$REPO_ROOT" branch -f production origin/production
}

sync_server() {
    read -rp "Do you want to update $DEPLOY_TARGET server files from origin/$DEPLOY_BRANCH? (y/n): " update_server
    if [[ "$update_server" != "y" ]]; then
        return
    fi

    echo "Updating $SERVER:$APP_DIR to origin/$DEPLOY_BRANCH..."
    ssh "$SERVER" "cd '$APP_DIR' && git fetch origin '$DEPLOY_BRANCH' && git checkout '$DEPLOY_BRANCH' && git reset --hard 'origin/$DEPLOY_BRANCH'"

    read -rp "Copy ignored config/cache files to $DEPLOY_TARGET? This may overwrite remote .env. (y/n): " copy_ignored
    if [[ "$copy_ignored" != "y" ]]; then
        echo "Ignored file copy skipped."
        return
    fi

    echo "Copying ignored files..."
    FILES_TO_COPY=(
        ".env"
    )

    cd "$REPO_ROOT"
    for f in "${FILES_TO_COPY[@]}"; do
        if [[ -d "$f" ]]; then
            echo "Copying directory $f"
            ssh "$SERVER" "mkdir -p '$REMOTE_PATH/$f'"
            scp -r "$f" "$SERVER:$REMOTE_PATH/$(dirname "$f")/"
        elif [[ -f "$f" ]]; then
            echo "Copying file $f"
            ssh "$SERVER" "mkdir -p '$REMOTE_PATH/$(dirname "$f")'"
            scp "$f" "$SERVER:$REMOTE_PATH/$f"
        else
            echo "Skipping missing path: $f"
        fi
    done
}

restart_services() {
    read -rp "Do you want to restart any services? (y/n): " restart_any
    if [[ "$restart_any" != "y" ]]; then
        echo "Service restarts skipped."
        return
    fi

    echo "Service restart options:"
    for i in "${!ACTIVE_SERVICES[@]}"; do
        printf "  %2d) %s\n" "$((i + 1))" "${ACTIVE_SERVICES[$i]}"
    done

    read -rp "Enter service numbers to restart (space/comma separated, blank to skip): " service_selection
    service_selection=${service_selection//,/ }
    if [[ -z "${service_selection// }" ]]; then
        echo "No services selected."
        return
    fi

    declare -A restarted=()
    for selection in $service_selection; do
        if [[ ! "$selection" =~ ^[0-9]+$ ]]; then
            echo "Skipping invalid entry: $selection"
            continue
        fi

        local idx=$((selection - 1))
        if (( idx < 0 || idx >= ${#ACTIVE_SERVICES[@]} )); then
            echo "Skipping out-of-range selection: $selection"
            continue
        fi

        local service="${ACTIVE_SERVICES[$idx]}"
        if [[ -n "${restarted[$service]:-}" ]]; then
            echo "Already restarted $service (skipping duplicate selection)"
            continue
        fi

        ssh -tt "$SERVER" "sudo systemctl restart '$service'"
        restarted[$service]=1
        echo "Restarted $service"
    done
}

main() {
    local proceed

    ensure_git_repo
    fetch_branches
    prompt_for_target
    SKIP_PROMOTION=0

    if [[ "$DEPLOY_TARGET" == "production" ]]; then
        list_promotable_commits
        prompt_for_commit_selection

        if [[ "$SKIP_PROMOTION" -eq 0 ]]; then
            echo
            echo "Selected commits:"
            printf "  %s\n" "${SELECTED_COMMITS[@]}"
            echo

            read -rp "Promote these commits to production now? (y/n): " proceed
            if [[ "$proceed" != "y" ]]; then
                echo "Deployment cancelled."
                exit 0
            fi

            prepare_production_worktree
            promote_commits_to_production
            push_production_branch
        else
            echo
            read -rp "Skip commit promotion and continue with current origin/production? (y/n): " proceed
            if [[ "$proceed" != "y" ]]; then
                echo "Deployment cancelled."
                exit 0
            fi
        fi
    else
        echo
        read -rp "Deploy latest origin/main to staging? (y/n): " proceed
        if [[ "$proceed" != "y" ]]; then
            echo "Deployment cancelled."
            exit 0
        fi
    fi
    sync_server
    restart_services
}

main "$@"
