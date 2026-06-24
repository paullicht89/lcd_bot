# Server Setup

These notes assume a Linux server with nginx already installed.

## Recommended Paths

```text
/srv/lcd_bot
/srv/lcd_bot/.venv
/srv/lcd_bot/.env
```

Run the app as a dedicated service user such as `lcdbot`.

## Install

```bash
cd /srv/lcd_bot
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
cp env.example .env
nano .env
```

Set `BOT_HOST=127.0.0.1` and `BOT_PORT=3978`. Keep the service bound locally and let nginx handle public HTTPS.

## systemd Unit

Create `/etc/systemd/system/lcd_bot.service`:

```ini
[Unit]
Description=LCD Teams Bot
After=network-online.target

[Service]
Type=simple
User=lcdbot
Group=lcdbot
WorkingDirectory=/srv/lcd_bot
Environment=PYTHONPATH=/srv/lcd_bot/src
ExecStart=/srv/lcd_bot/.venv/bin/python -m lcd_teams_bot.app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now lcd_bot
sudo systemctl status lcd_bot
```

## nginx Site

Example server block:

```nginx
server {
    listen 80;
    server_name lcdbot.lcd.nyc;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name lcdbot.lcd.nyc;

    ssl_certificate /etc/letsencrypt/live/lcdbot.lcd.nyc/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/lcdbot.lcd.nyc/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:3978;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Reload nginx after testing:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Verification

```bash
curl https://lcdbot.lcd.nyc/healthz
journalctl -u lcd_bot -f
```

Then set Azure Bot Service messaging endpoint to:

```text
https://lcdbot.lcd.nyc/api/messages
```

## Operational Notes

- Rotate `MicrosoftAppPassword` periodically and update `.env`.
- Add firewall rules so only ports 80/443 are public.
- Keep `/api/messages` public over HTTPS because Bot Framework must call it.
- Store future conversation references under an ignored `data/` path if proactive messaging is added.
- Local deploy helper defaults live in `scripts/deploy/README.md`.
