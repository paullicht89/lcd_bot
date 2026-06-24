from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)


@dataclass(frozen=True)
class Settings:
    microsoft_app_type: str = os.getenv("MicrosoftAppType", "SingleTenant")
    microsoft_app_id: str = os.getenv("MicrosoftAppId", "")
    microsoft_app_password: str = os.getenv("MicrosoftAppPassword", "")
    microsoft_app_tenant_id: str = os.getenv("MicrosoftAppTenantId", "")
    host: str = os.getenv("BOT_HOST", "127.0.0.1")
    port: int = int(os.getenv("BOT_PORT", "3978"))
    public_base_url: str = os.getenv("BOT_PUBLIC_BASE_URL", "https://lcdbot.lcd.nyc")
    environment: str = os.getenv("ENVIRONMENT", "local")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    nys_app_token: str = os.getenv("NYS_APP_TOKEN", "")


settings = Settings()
