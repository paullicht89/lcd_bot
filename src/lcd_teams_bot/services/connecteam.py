from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any

from lcd_teams_bot.config import settings

USERS_URL = "https://api.connecteam.com/users/v1/users"
PAGE_SIZE = 500


class ConnecteamError(RuntimeError):
    """Raised when Connecteam user data cannot be retrieved."""


def normalize_phone(value: Any) -> str:
    digits = "".join(character for character in str(value or "") if character.isdigit())
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) != 10:
        raise ValueError("Phone number must contain 10 digits.")
    return f"+1{digits}"


def _clean(value: Any) -> str:
    return " ".join(str(value or "").casefold().split())


def _name_matches(user: dict[str, Any], first_name: str, last_name: str) -> bool:
    requested = [_clean(first_name), _clean(last_name)]
    actual = [_clean(user.get("firstName")), _clean(user.get("lastName"))]
    for needle, candidate in zip(requested, actual):
        if not needle:
            continue
        if needle in candidate or candidate in needle:
            continue
        if SequenceMatcher(None, needle, candidate).ratio() >= 0.72:
            continue
        return False
    return True


async def search_connecteam_users(values: dict[str, Any]) -> list[dict[str, Any]]:
    first_name = str(values.get("first_name") or "").strip()
    last_name = str(values.get("last_name") or "").strip()
    phone = str(values.get("phone_number") or "").strip()

    params: dict[str, Any] = {"limit": PAGE_SIZE, "offset": 0, "userStatus": "all"}
    full_name = " ".join(part for part in (first_name, last_name) if part)
    if full_name:
        params["fullNames"] = full_name
    if phone:
        params["phoneNumbers"] = normalize_phone(phone)

    users, _ = await _get_users_page(params)
    if users or not full_name:
        return users

    all_users = await _get_all_users()
    return [user for user in all_users if _name_matches(user, first_name, last_name)]


async def _get_all_users() -> list[dict[str, Any]]:
    users: list[dict[str, Any]] = []
    offset = 0
    while True:
        page, total = await _get_users_page(
            {"limit": PAGE_SIZE, "offset": offset, "userStatus": "all"}
        )
        users.extend(page)
        offset += len(page)
        if not page or offset >= total:
            return users


async def _get_users_page(params: dict[str, Any]) -> tuple[list[dict[str, Any]], int]:
    import aiohttp

    if not settings.connecteam_api_key:
        raise ConnecteamError("CONNECTEAM_API_KEY is not configured.")

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": settings.connecteam_api_key,
    }
    try:
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(USERS_URL, headers=headers, params=params) as response:
                if response.status >= 400:
                    raise ConnecteamError(f"Connecteam lookup returned HTTP {response.status}.")
                payload = await response.json()
    except aiohttp.ClientError as exc:
        raise ConnecteamError("Connecteam lookup request failed.") from exc
    except ValueError as exc:
        raise ConnecteamError("Connecteam lookup returned invalid JSON.") from exc

    try:
        raw_users = payload["data"]["users"]
        total = int(payload.get("paging", {}).get("total", len(raw_users)))
    except (KeyError, TypeError, ValueError) as exc:
        raise ConnecteamError("Connecteam lookup returned an unexpected response shape.") from exc
    return [user for user in raw_users if isinstance(user, dict)], total


def custom_field_value(user: dict[str, Any], custom_field_id: int) -> str:
    for field in user.get("customFields") or []:
        if isinstance(field, dict) and field.get("customFieldId") == custom_field_id:
            value = field.get("value")
            return str(value).strip() if value not in (None, "") else "N/A"
    return "N/A"
