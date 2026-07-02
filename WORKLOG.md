# Worklog

## 2026-07-02

- Added `/pwgen` random temporary password command using a production-local generator based on the reference password script format.
- Added Adaptive Card output for generated passwords with `Generate Another Password` and `Done` actions.
- Registered `/pwgen` in command/help flows, Teams manifest command list, README, changelog, and tests.

## 2026-06-25

- Added `/nyslic` guided NYS Elevator License lookup for individual and business licenses.
- Added Adaptive Card chooser, individual/business search forms, and result tables with license type label conversions.
- Added NYS license service module for data.ny.gov individual and business POST query endpoints.
- Added tests for `/nyslic` registration, card wiring, query construction, and result formatting.

## 2026-06-24

- Created the initial standalone LCD Teams Bot scaffold.
- Established Python/FastAPI/Bot Framework project shape under `src/lcd_teams_bot/`.
- Added starter command registry for `help`, `ping`, `status`, and `lookup`.
- Added Adaptive Card builder for lookup prompts.
- Added Teams app manifest template and packaging script.
- Added Microsoft/Teams and server deployment setup docs.
- Added phase 1 operational logging and generic bot error handling without persistence.
- Added local Teams package validation to troubleshoot Admin Center manifest upload errors.
- Matched the LCD Bot Teams package icon layout to the working HRIS app package.
- Aligned Teams manifest developer links with stable company pages used by the working HRIS package.
- Documented the Teams install error that indicates an unregistered bot or missing Teams channel.
- Added `/dobinsp` guided DOB Now Safety inspection lookup cards and API integration.
- Added `/ecblookup` guided ECB violation lookup with Adaptive Card search/results, DOB link/image buttons, and data.cityofnewyork.us API integration.
- Converted `help` to an Adaptive Card command catalog and added `commands`/`menu` aliases.

## Next Work

- Create Azure Bot resource and single-tenant app identity.
- Fill in `teams/lcd_bot/manifest.json` IDs and production host values.
- Decide the final hostname, likely `lcdbot.lcd.nyc`.
- Add persistent storage for conversation references if proactive messages are needed.
