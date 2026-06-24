# Deploy Scripts

## Files

- `push.sh` - interactively stages, commits, logs, and optionally pushes the current branch.
- `deploy.sh` - promotes selected commits from `main` to `production`, syncs the server, and restarts services.
- `GIT_LOG.md` - reference template. Runtime commit logs are written to ignored `.local/GIT_LOG.md`.

## Defaults

- SSH server alias: `lcd-do-hris`
- Production app path: `/srv/lcd_bot`
- Production service: `lcd_bot`
- Staging app path: `/srv/lcd_bot-staging`
- Staging service: `lcd_bot-staging`

Override defaults with environment variables:

```bash
export LCD_BOT_DEPLOY_SERVER=your-ssh-alias
export LCD_BOT_PROD_APP_DIR=/srv/lcd_bot
export LCD_BOT_PROD_SERVICE=lcd_bot
export LCD_BOT_STAGING_APP_DIR=/srv/lcd_bot-staging
export LCD_BOT_STAGING_SERVICE=lcd_bot-staging
```

## One-Time Branch Setup

This repo currently uses `main` for normal work. The production deploy flow expects `origin/production` to exist.

Create it once when `main` is in a deployable state:

```bash
git checkout main
git pull origin main
git checkout -b production
git push -u origin production
git checkout main
```

After that, keep working on `main`. Use `deploy.sh` to select commits from `main` and cherry-pick them onto `production`.

## Server Pre-Work

On the server, make sure:

- The repo is cloned into `/srv/lcd_bot`.
- The remote server can fetch from GitHub.
- `/srv/lcd_bot/.env` exists with production secrets.
- The `lcd_bot` systemd service exists and starts the app.
- nginx proxies `https://lcdbot.lcd.nyc` to `127.0.0.1:3978`.

Use `docs/deployment/server_setup.md` for the service and nginx examples.

## Initial Deploy With No New Commits

If `main` and `production` are identical, `deploy.sh` will report that no commits are waiting and then let you continue with current `origin/production`.

For the first server setup:

1. Clone the repo on the server:

   ```bash
   sudo mkdir -p /srv/lcd_bot
   sudo chown "$USER":"$USER" /srv/lcd_bot
   git clone -b production git@github.com:paullicht89/lcd_bot.git /srv/lcd_bot
   cd /srv/lcd_bot
   python3 -m venv .venv
   . .venv/bin/activate
   python -m pip install -r requirements.txt
   cp env.example .env
   nano .env
   ```

2. Run `scripts/deploy/deploy.sh` locally.
3. Choose `production`.
4. Continue with current `origin/production`.
5. Say `y` if you want the script to copy your local ignored `.env` to the server.
6. Restart `lcd_bot` when prompted.

If you create `.env` directly on the server, answer `n` to the ignored-file copy prompt.
