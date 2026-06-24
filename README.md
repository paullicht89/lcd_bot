# LCD Teams Bot

Internal Microsoft Teams bot for LCD Elevator command workflows. Users will open the bot in Teams, run a command, answer Adaptive Card prompts, and retrieve data or trigger approved automations.

This repo is intentionally separate from the HRIS app. The previous HRIS bot examples under `example_files/` are reference material only; new bot code should live under `src/lcd_teams_bot/`.

## Planned Capabilities

- Teams personal and team-scope bot commands.
- Adaptive Card prompts for guided inputs and confirmations.
- Data lookups from Microsoft Graph, Connecteam, Dataverse, NYC/NYS public APIs, and future internal services.
- Automation actions with confirmation steps before state-changing work.
- Server deployment behind nginx at a dedicated hostname such as `lcdbot.lcd.nyc`.

## Project Layout

- `src/lcd_teams_bot/` - FastAPI/Bot Framework service.
- `src/lcd_teams_bot/commands/` - command registry and command handlers.
- `src/lcd_teams_bot/cards/` - Adaptive Card builders.
- `teams/lcd_bot/` - Teams app manifest package source.
- `config/` - non-secret config templates and future command catalogs.
- `docs/deployment/` - Microsoft, Teams, nginx, and server setup notes.
- `docs/sample_api/` - API notes and examples used when adding command integrations.
- `scripts/` - local run and Teams package helper scripts.
- `tests/` - pytest tests.

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item env.example .env
```

Edit `.env` with the bot registration values from Azure/Microsoft:

- `MicrosoftAppType=SingleTenant`
- `MicrosoftAppId=<bot app/client id>`
- `MicrosoftAppPassword=<client secret value>`
- `MicrosoftAppTenantId=<tenant id>`
- `BOT_PUBLIC_BASE_URL=https://lcdbot.lcd.nyc`

Run locally:

```powershell
.\scripts\run_local.ps1
```

The service exposes:

- `GET /healthz` - health check.
- `POST /api/messages` - Bot Framework messaging endpoint.

Runtime logs are written to stdout for local shells and `systemd`/journald. Set `LOG_LEVEL`
in `.env` to control verbosity. Request logs avoid raw Teams message text and card payloads.

For local Teams testing, expose the service with a trusted tunnel and set the Azure Bot messaging endpoint to `https://<public-host>/api/messages`.

## Initial Commands

- `help` or `/help` - show available commands.
- `ping` or `/ping` - verify the bot is reachable.
- `status` or `/status` - show current service/environment status.
- `lookup` or `/lookup` - starter Adaptive Card flow for future data lookups.

## Teams App Package

1. Register the bot in Azure Bot Service and note the app/client ID.
2. Replace every placeholder in `teams/lcd_bot/manifest.json`, especially:
   - `REPLACE-WITH-TEAMS-APP-ID`
   - `REPLACE-WITH-BOT-APP-ID`
   - URLs under `developer` and `validDomains`
3. Package the Teams app:

```powershell
.\scripts\package_teams_app.ps1
```

4. Upload the generated zip through Teams developer tools or the Teams admin center app catalog.

## Deployment Direction

Recommended hostname: `lcdbot.lcd.nyc`.

Recommended public endpoint: `https://lcdbot.lcd.nyc/api/messages`.

Use a dedicated Linux service account and run the app with uvicorn behind nginx. See [docs/deployment/server_setup.md](docs/deployment/server_setup.md) and [docs/deployment/microsoft_setup.md](docs/deployment/microsoft_setup.md).

## Development Rules

- Keep secrets out of git. `.env` is ignored.
- Add new Teams commands through `src/lcd_teams_bot/commands/registry.py`.
- Use Adaptive Cards for multi-step prompts and confirmations.
- Require explicit user confirmation before commands mutate external systems.
- Document every meaningful change in `CHANGELOG.md` and active work in `WORKLOG.md`.
