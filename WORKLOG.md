# Worklog

## 2026-06-24

- Created the initial standalone LCD Teams Bot scaffold.
- Established Python/FastAPI/Bot Framework project shape under `src/lcd_teams_bot/`.
- Added starter command registry for `help`, `ping`, `status`, and `lookup`.
- Added Adaptive Card builder for lookup prompts.
- Added Teams app manifest template and packaging script.
- Added Microsoft/Teams and server deployment setup docs.

## Next Work

- Create Azure Bot resource and single-tenant app identity.
- Fill in `teams/lcd_bot/manifest.json` IDs and production host values.
- Decide the final hostname, likely `lcdbot.lcd.nyc`.
- Add first real lookup command using one of the documented APIs under `docs/sample_api/`.
- Add persistent storage for conversation references if proactive messages are needed.
