# Agent Notes: LCD Teams Bot

## Mission

Build a standalone Microsoft Teams bot for LCD Elevator. It should stay independent from the HRIS app while borrowing proven patterns from `example_files/` when helpful.

## Architecture

- Runtime: Python, FastAPI, Bot Framework SDK.
- Entry point: `src/lcd_teams_bot/app.py`.
- Commands: `src/lcd_teams_bot/commands/registry.py`.
- Cards: `src/lcd_teams_bot/cards/`.
- Teams package source: `teams/lcd_bot/`.
- Deployment docs: `docs/deployment/`.

## Guardrails

- Do not edit or depend on `example_files/` for production behavior. Treat it as read-only reference.
- Do not commit secrets, tenant IDs, app IDs, client secrets, tokens, production URLs with secret query strings, exported chat data, or conversation reference files.
- Keep user-facing Teams flows concise. Prefer Adaptive Cards for collecting inputs over free-form parsing when a command has required parameters.
- Any command that writes data, sends messages, creates records, updates shifts, or triggers automation must show a confirmation step first.
- Keep integrations behind small service modules as they are added. Command handlers should orchestrate, not become API clients.
- Update `WORKLOG.md` during active work and `CHANGELOG.md` for user-visible or operational changes.

## Local Commands

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
.\scripts\run_local.ps1
pytest -q
```

## Microsoft/Teams Notes

- Prefer `MicrosoftAppType=SingleTenant` for this internal company bot.
- Bot endpoint should be `/api/messages`.
- Public production endpoint should use HTTPS, for example `https://lcdbot.lcd.nyc/api/messages`.
- Teams manifest placeholders must be replaced before packaging.

## Documentation References

- `README.md` - project overview and local setup.
- `docs/deployment/microsoft_setup.md` - Azure Bot, app registration, Graph, and Teams app catalog steps.
- `docs/deployment/server_setup.md` - nginx, systemd, and production environment notes.
- `docs/sample_api/` - early API research for future lookup commands.
