# Worklog

## 2026-09-24

- Added `/splashtoppc` search, submit/cancel, device results, and search-again Adaptive Cards.
- Added a read-only Splashtop service with environment-based credentials/team ID, query parameters for either or both inputs, input validation, timeouts, and sanitized failures.
- Registered the command in help and the Teams manifest; documented environment setup and both-field behavior.
- Verified with the project virtual environment: 65 pytest tests passed, Teams package validation passed, and diff whitespace checks passed. Tests cover request parameters, validation, transport/API errors, device rendering, batching, cancellation, and retry. No live API credentials used.

## 2026-08-31

- Added `/maptiveup` with an explicit confirmation card and authenticated Fieldboss Automations webhook call.
- Added user-facing success and actionable error responses without exposing the Maptive sync secret.
- Registered `/maptiveup` in help, the Teams manifest, README, changelog, environment template, and tests.
- Expanded the `help` Adaptive Card to the full Teams message width for easier reading.
- Expanded `/maptiveup` with a Maptive/Dataverse selection card, Submit/Cancel actions, and the authenticated Dataverse `ALL` sync webhook.
- Updated the Maptive sync webhook to send the same `{"scope": "ALL"}` JSON payload.

## 2026-08-03

- Added `/eei` employee ID lookup with Adaptive Card search, disambiguation, and result views.
- Added Connecteam exact name/phone lookup plus paginated fuzzy name fallback.
- Registered `/eei` in help, Teams manifest, README, changelog, and tests.

## 2026-07-02

- Added `/pwgen` random temporary password command using a production-local generator based on the reference password script format.
- Added Adaptive Card output for generated passwords with `Generate Another Password` and `Done` actions.
- Registered `/pwgen` in command/help flows, Teams manifest command list, README, changelog, and tests.
- Updated `/pwgen` to use the revised reference word list and `Word-Word-Word-##Symbol` format.
- Added run buttons to the `help` command catalog so users can launch commands from the Adaptive Card.

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
