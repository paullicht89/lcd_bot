# GIT_LOG

## Purpose

Local tracking of git commits and branches, most recent history only.

## Template

```text
YYYY-MM-DD HH:mm:ss | branch | commit hash/number | message here
```

## Commands to Remember

- `git log --oneline production..main`
- `git show <hash>`
- `git log --oneline`
- `git log --reverse --oneline production..main`
- `git branch --show-current`
- `git remote -v`

## If Cherry-Pick Conflict Occurs

- `git status`
- `git add <resolved files>`
- `git cherry-pick --continue` or abort with `git cherry-pick --abort`

## Create Production Branch Once

```bash
git checkout main
git pull origin main
git checkout -b production
git push -u origin production
git checkout main
```

## LCD Bot Defaults

- Normal development branch: `main`
- Deployment promotion branch: `production`
- Production server path: `/srv/lcd_bot`
- Production service: `lcd_bot`

## Commit History

No LCD Bot deployment commits logged yet.
