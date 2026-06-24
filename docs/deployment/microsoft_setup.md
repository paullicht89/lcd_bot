# Microsoft and Teams Setup

Use this as the first-pass checklist for creating the bot identity and installing it in Teams.

## Recommended Names

- Public hostname: `lcdbot.lcd.nyc`
- Bot display name: `LCD Bot`
- Messaging endpoint: `https://lcdbot.lcd.nyc/api/messages`
- App type: `SingleTenant`

## 1. Create the Azure Bot

1. In Azure Portal, create an Azure Bot resource.
2. Choose single-tenant identity for LCD's Microsoft tenant.
3. Record:
   - Microsoft App ID / client ID.
   - Tenant ID.
   - Client secret value.
4. Set the messaging endpoint to `https://lcdbot.lcd.nyc/api/messages`.
5. Enable the Microsoft Teams channel for the bot.

Environment mapping:

```text
MicrosoftAppType=SingleTenant
MicrosoftAppId=<Azure Bot app/client ID>
MicrosoftAppPassword=<client secret value>
MicrosoftAppTenantId=<tenant ID>
```

Microsoft's Azure Bot registration docs note that new multi-tenant bot creation is deprecated after July 31, 2025. For this internal company bot, single-tenant is the right default.

## 2. Configure Graph Permissions When Needed

Only add Graph permissions as commands require them. Start small.

Likely future application permissions:

- `User.Read.All` for directory/user lookup.
- `Sites.Read.All` or `Sites.ReadWrite.All` for SharePoint lookups or file actions.
- `ChannelMessage.Send` or resource-specific consent only if the bot must proactively post into channels.

After adding application permissions, an admin must grant consent.

## 3. Prepare the Teams Manifest

1. Open `teams/lcd_bot/manifest.json`.
2. Replace `REPLACE-WITH-TEAMS-APP-ID` with a new GUID for the Teams app package.
3. Replace `REPLACE-WITH-BOT-APP-ID` with the Azure Bot Microsoft App ID.
4. Confirm `validDomains` contains `lcdbot.lcd.nyc`.
5. Confirm command names match `src/lcd_teams_bot/commands/registry.py`.

## 4. Package and Upload

```powershell
.\scripts\package_teams_app.ps1
```

Upload `dist/lcd-teams-bot.zip` to Teams for testing or publish it through the Teams admin center app catalog.

If Teams says it cannot read `manifest.json`, run:

```powershell
python .\scripts\validate_teams_package.py .\dist\lcd-teams-bot.zip
```

Then confirm you are uploading `dist/lcd-teams-bot.zip` itself, not the unpacked `dist/lcd-teams-bot-package` folder or a zip that contains that folder as the root.

If Teams says `Please make sure the bot is registered and teams' channel is enabled`, the app package was readable but Teams could not resolve the bot ID as a Teams-enabled Bot Framework bot. Check:

1. `teams/lcd_bot/manifest.json` `bots[0].botId` exactly matches the Azure Bot Microsoft App ID / client ID.
2. The Azure Bot resource exists. An Entra app registration by itself is not enough for Teams bot installation.
3. The Azure Bot resource has the Microsoft Teams channel enabled under **Channels**.
4. The Azure Bot messaging endpoint is set to `https://lcdbot.lcd.nyc/api/messages`.
5. If the bot was just created or the Teams channel was just enabled, wait a few minutes and retry the upload/install.

## 5. Smoke Test

In Teams:

1. Install/open `LCD Bot`.
2. Send `ping`; expect `pong`.
3. Send `status`; expect environment details.
4. Send `lookup`; expect an Adaptive Card.

If messages do not arrive, check:

- Azure Bot messaging endpoint.
- nginx HTTPS certificate and proxy config.
- systemd service logs.
- `.env` values on the server.
