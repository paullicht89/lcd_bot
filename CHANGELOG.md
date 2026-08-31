# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

### Added

- Added `/maptiveup` to force a confirmed Maptive data update through Fieldboss Automations.
- Added Dataverse as an `/maptiveup` update target with an `ALL` scope sync payload.
- Added `/eei` Connecteam employee ID lookup with name/phone search and user selection cards.
- Added `/pwgen` random temporary password generation with Adaptive Card actions.
- Added `/nyslic` NYS Elevator License lookup for individual and business licenses with Adaptive Card search and results.
- Added run buttons to the `help` Adaptive Card command catalog.

### Changed

- Expanded the `help` Adaptive Card to the full Teams message width.
- Updated the Maptive force-update request to send an `ALL` scope payload.

## [0.1.0] - 2026-06-24

### Added

- Initial standalone Teams bot repository scaffold.
- FastAPI/Bot Framework service with `/healthz` and `/api/messages`.
- Starter commands: `help`, `ping`, `status`, and `lookup`.
- Adaptive Card prompt skeleton for lookup workflows.
- Teams manifest template for the LCD Teams Bot.
- Local run script and Teams package script.
- Teams package validator for manifest, icon, placeholder, and zip structure checks.
- Flat Teams app package icon layout matching the working HRIS app package.
- Environment template and deployment documentation.

### Changed

- Teams manifest developer URLs now use stable company pages during app catalog upload.
- Added stdout/journald-friendly logging and generic Bot Framework error handling.
- Added `/dobinsp` guided DOB Now Safety lookup flow with Adaptive Card results.
- Added `/ecblookup` guided ECB violation lookup flow with Adaptive Card results and DOB link/image buttons.
- Changed `help` to return an Adaptive Card command catalog and added `commands`/`menu` aliases.
