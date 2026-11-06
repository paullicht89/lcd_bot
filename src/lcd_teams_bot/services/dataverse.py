from __future__ import annotations

import asyncio
import logging
from urllib.parse import quote, urlsplit

import aiohttp

from lcd_teams_bot.config import settings

logger = logging.getLogger(__name__)


class DataverseError(RuntimeError):
    """Dataverse lookup failed; upstream details must not be shown in Teams."""

    def __init__(self, message: str, *, reason: str = "invalid_response", status: int | None = None) -> None:
        super().__init__(message)
        # Only controlled reason codes and HTTP status; never exception text or response bodies.
        logger.warning("Dataverse lookup failed: reason=%s status=%s", reason, status)
        self.user_message = {
            "missing_credentials": "Dataverse access is not configured. Ask IT to set DATAVERSE_TENANT_ID, DATAVERSE_CLIENT_ID, and DATAVERSE_CLIENT_SECRET, then restart the bot.",
            "invalid_url": "Dataverse URL is invalid. Ask IT to check DATAVERSE_URL and restart the bot.",
            "token_request": "Dataverse sign-in failed. Ask IT to check the Dataverse application credentials and server logs.",
            "unauthorized": "Dataverse rejected the access token. Ask IT to check token expiry and the Dataverse environment. If DATAVERSE_ACCESS_TOKEN is set, replace it or clear it to use application credentials, then restart the bot.",
            "forbidden": "Dataverse denied access. Ask IT to check the application user's security role and User table read access.",
            "throttled": "Dataverse is busy. Please wait a moment and try again.",
            "transport": "Could not connect to Dataverse or read its response. Please try again; IT can check the server logs.",
        }.get(reason, "Could not retrieve Fieldboss users. Please try again or ask IT to check the Dataverse server logs.")


def build_user_params(values: dict) -> dict[str, str]:
    names = []
    for key in ("first_name", "last_name"):
        value = values.get(key, "")
        if value is None:
            value = ""
        if not isinstance(value, str) or len(value) > 100:
            raise ValueError("Enter names as text, up to 100 characters each.")
        names.append(value.strip().replace("'", "''"))
    if not any(names):
        raise ValueError("Please enter a First Name or Last Name to search.")
    return {
        "$select": "fullname,systemuserid,domainname",
        "$filter": (
            f"contains(firstname,'{names[0]}') and contains(lastname,'{names[1]}') "
            "and contains(domainname,'@lcdelevator.')"
        ),
        "$orderby": "fullname,systemuserid",
    }


async def _access_token(session: aiohttp.ClientSession, base_url: str) -> str:
    if settings.dataverse_access_token.strip():
        return settings.dataverse_access_token.strip()
    if not all(value.strip() for value in (settings.dataverse_tenant_id, settings.dataverse_client_id,
                                          settings.dataverse_client_secret)):
        missing = [name for name, value in (
            ("DATAVERSE_TENANT_ID", settings.dataverse_tenant_id),
            ("DATAVERSE_CLIENT_ID", settings.dataverse_client_id),
            ("DATAVERSE_CLIENT_SECRET", settings.dataverse_client_secret),
        ) if not value.strip()]
        logger.warning("Dataverse configuration missing: %s", ", ".join(missing))
        raise DataverseError("Dataverse authentication is not configured.", reason="missing_credentials")
    tenant = quote(settings.dataverse_tenant_id, safe="")
    async with session.post(
        f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token",
        data={"grant_type": "client_credentials", "client_id": settings.dataverse_client_id,
              "client_secret": settings.dataverse_client_secret, "scope": f"{base_url}/.default"},
        allow_redirects=False,
    ) as response:
        if response.status != 200:
            raise DataverseError("Dataverse authentication failed.", reason="token_request", status=response.status)
        payload = await response.json()
    token = payload.get("access_token") if isinstance(payload, dict) else None
    if not isinstance(token, str) or not token.strip():
        raise DataverseError("Dataverse authentication returned no token.")
    return token


async def search_dataverse_users(values: dict) -> list[dict]:
    params = build_user_params(values)
    base_url = settings.dataverse_url.strip().rstrip("/")
    try:
        parsed = urlsplit(base_url)
    except ValueError as exc:
        raise DataverseError("Invalid Dataverse URL.", reason="invalid_url") from exc
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
            or parsed.path or parsed.query or parsed.fragment):
        raise DataverseError("Configure DATAVERSE_URL as an HTTPS environment origin.", reason="invalid_url")
    endpoint = f"{base_url}/api/data/v9.2/systemusers"
    rows: list[dict] = []
    seen: set[str] = set()
    url = endpoint
    stage = "authentication"
    logger.info("Dataverse lookup started: auth_mode=%s",
                "bearer_token" if settings.dataverse_access_token.strip() else "client_credentials")
    try:
        async with asyncio.timeout(60), aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=20)
        ) as session:
            token = await _access_token(session, base_url)
            stage = "systemusers"
            headers = {
                "Authorization": f"Bearer {token}", "Accept": "application/json",
                "OData-Version": "4.0", "OData-MaxVersion": "4.0",
                "Prefer": 'odata.include-annotations="OData.Community.Display.V1.FormattedValue"',
            }
            while url:
                # Only send credentials to the original collection, including on subsequent pages.
                next_url = urlsplit(url)
                if (next_url.scheme != parsed.scheme or next_url.netloc != parsed.netloc
                        or next_url.path != urlsplit(endpoint).path or next_url.fragment or url in seen):
                    raise DataverseError("Dataverse returned an invalid continuation link.")
                seen.add(url)
                async with session.get(url, params=params, headers=headers, allow_redirects=False) as response:
                    if response.status != 200:
                        reason = {401: "unauthorized", 403: "forbidden", 429: "throttled"}.get(response.status, "query_http")
                        raise DataverseError("Dataverse user lookup failed.", reason=reason, status=response.status)
                    payload = await response.json()
                page = payload.get("value") if isinstance(payload, dict) else None
                if not isinstance(page, list) or any(not isinstance(row, dict) for row in page):
                    raise DataverseError("Dataverse returned an invalid user list.")
                rows.extend(page)
                url = payload.get("@odata.nextLink", "")
                if not isinstance(url, str):
                    raise DataverseError("Dataverse returned an invalid continuation link.")
                params = None
    except (aiohttp.ClientError, TimeoutError, ValueError) as exc:
        logger.warning("Dataverse request failed: stage=%s exception_type=%s", stage, type(exc).__name__)
        raise DataverseError("Dataverse request failed.", reason="transport") from exc
    logger.info("Dataverse lookup completed: pages=%s results=%s", len(seen), len(rows))
    return rows
