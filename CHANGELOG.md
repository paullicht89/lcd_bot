# Changelog

All notable changes to this project will be documented here.

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
