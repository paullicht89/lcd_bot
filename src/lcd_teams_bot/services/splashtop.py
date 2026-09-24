from __future__ import annotations

from typing import Any

import aiohttp

from lcd_teams_bot.config import settings


class SplashtopError(RuntimeError):
    """Raised when Splashtop device information cannot be retrieved."""


def build_computer_params(values: dict[str, Any]) -> dict[str, str]:
    params = {}
    for field, parameter in (("id", "ids"), ("host_name", "host_name")):
        value = values.get(field)
        if value is None:
            continue
        if not isinstance(value, str):
            raise ValueError("Enter an ID or Host Name as text.")
        if value.strip():
            params[parameter] = value.strip()
    if not params:
        raise ValueError("Please enter an ID or Host Name to search.")
    if "ids" in params and not (params["ids"].isascii() and params["ids"].isdigit()):
        raise ValueError("Please enter a numeric device ID.")
    return params


async def search_splashtop_computers(values: dict[str, Any]) -> list[dict[str, Any]]:
    params = build_computer_params(values)
    team_id = settings.splashtop_team_id.strip()
    token = settings.splashtop_api_token.strip()
    if not token or not (team_id.isascii() and team_id.isdigit()):
        raise SplashtopError("Splashtop integration is not configured.")

    url = f"https://webapi.splashtop.com/api/open/v1/teams/{team_id}/computers"
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20)) as session:
            async with session.get(
                url, params=params, headers={"Authorization": f"Bearer {token}"},
                allow_redirects=False,
            ) as response:
                if response.status != 200:
                    raise SplashtopError("Splashtop lookup returned an unsuccessful HTTP status.")
                payload = await response.json()
    except (aiohttp.ClientError, TimeoutError, ValueError) as exc:
        raise SplashtopError("Splashtop lookup request failed.") from exc

    if not isinstance(payload, dict) or payload.get("result") != 20200:
        raise SplashtopError("Splashtop lookup returned an unsuccessful result.")
    rows = payload.get("data")
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise SplashtopError("Splashtop lookup returned an invalid device list.")
    return rows
