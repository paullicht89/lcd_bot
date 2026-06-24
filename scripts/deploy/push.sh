#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_STATE_DIR="$SCRIPT_DIR/.local"
GIT_LOG_FILE="$LOCAL_STATE_DIR/GIT_LOG.md"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

timestamp() {
    date +"%Y-%m-%d %H:%M:%S"
}

log_git_event() {
    local branch="$1"
    local commit_hash="$2"
    local message="$3"

    mkdir -p "$LOCAL_STATE_DIR"

    if [[ ! -f "$GIT_LOG_FILE" ]]; then
        cat > "$GIT_LOG_FILE" <<'EOF'
# GIT_LOG

## Purpose
Local tracking of git commits and branches, most recent history only.

## Template
```text
YYYY-MM-DD HH:mm:ss | branch | commit hash/number | message here
```

### Commands to Remember
- `git log --oneline production..main`
- `git show <hash>`
- `git log --oneline`
- `git log --reverse --oneline production..main`
- `git branch --show-current`
- `git remote -v`

### If Cherry-Pick Conflict Occurs
- `git status`
- `git add <resolved files>`
- `git cherry-pick --continue` or abort with `git cherry-pick --abort`

### Create Branch and Push Data
```bash
git checkout main
git pull origin main
git checkout -b production
git push -u origin production
git checkout main
```

### LCD Bot Defaults
- Normal development branch: `main`
- Deployment promotion branch: `production`
- Production server path: `/srv/lcd_bot`
- Production service: `lcd_bot`

## Commit History (Last 45 Days)

EOF
    fi

    if [[ -s "$GIT_LOG_FILE" ]] && [[ "$(tail -c 1 "$GIT_LOG_FILE" | tr -d '\n' | wc -c)" -ne 0 ]]; then
        printf '\n' >> "$GIT_LOG_FILE"
    fi

    printf '%s | %s | %s | %s\n' "$(timestamp)" "$branch" "$commit_hash" "$message" >> "$GIT_LOG_FILE"
}

ensure_git_repo() {
    git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
        echo "Not inside a Git repository."
        exit 1
    }
}

main() {
    local current_branch

    ensure_git_repo
    cd "$REPO_ROOT"

    current_branch="$(git branch --show-current)"

    echo "Current branch: $current_branch"
    echo "Git log file: $GIT_LOG_FILE"
    echo

    while true; do
        mapfile -t STATUS_LINES < <(git status --short)

        if [[ ${#STATUS_LINES[@]} -eq 0 ]]; then
            echo "No changes detected."
            break
        fi

        echo "Changed files:"
        for i in "${!STATUS_LINES[@]}"; do
            printf "  %2d) %s\n" "$((i + 1))" "${STATUS_LINES[$i]}"
        done
        echo
        echo "Choose files to stage:"
        echo "  a = all"
        echo "  q = quit without committing more"
        read -rp "Enter numbers separated by spaces (or 'a'/'q'): " SELECTION

        if [[ "$SELECTION" == "q" || "$SELECTION" == "Q" ]]; then
            echo "Exiting without additional commits."
            break
        fi

        if [[ "$SELECTION" == "a" || "$SELECTION" == "A" ]]; then
            git add .
        else
            for selection in $SELECTION; do
                if [[ ! "$selection" =~ ^[0-9]+$ ]]; then
                    echo "Invalid selection: $selection"
                    continue
                fi

                idx=$((selection - 1))
                if (( idx < 0 || idx >= ${#STATUS_LINES[@]} )); then
                    echo "Out-of-range selection: $selection"
                    continue
                fi

                line="${STATUS_LINES[$idx]}"
                file="${line:3}"
                git add -- "$file"
                echo "Staged: $file"
            done
        fi

        echo
        echo "Staged changes:"
        git diff --cached --name-only || true
        echo

        read -rp "Enter commit message (or leave blank to unstage and cancel this commit): " COMMIT_MSG

        if [[ -z "${COMMIT_MSG// }" ]]; then
            echo "Blank commit message. Unstaging selected files."
            git reset
        else
            git commit -m "$COMMIT_MSG"

            COMMIT_HASH="$(git rev-parse --short HEAD)"
            COMMIT_SUBJECT="$(git log -1 --pretty=%s)"
            BRANCH_NOW="$(git branch --show-current)"

            log_git_event "$BRANCH_NOW" "$COMMIT_HASH" "$COMMIT_SUBJECT"

            echo "Commit created: $COMMIT_HASH | $COMMIT_SUBJECT"
            echo "Logged to: $GIT_LOG_FILE"
        fi

        echo
        read -rp "Do you want to create another commit from remaining changes? (y/n): " AGAIN
        [[ "$AGAIN" =~ ^[Yy]$ ]] || break
        echo
    done

    current_branch="$(git branch --show-current)"
    read -rp "Do you want to push branch '$current_branch' to origin? (y/n): " PUSH_NOW

    if [[ "$PUSH_NOW" =~ ^[Yy]$ ]]; then
        git push origin "$current_branch"
        echo "Pushed '$current_branch' to origin."
    else
        echo "Push skipped."
    fi
}

main "$@"
