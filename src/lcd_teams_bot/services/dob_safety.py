from __future__ import annotations

from typing import Any

from lcd_teams_bot.config import settings

DOB_SAFETY_URL = "https://data.cityofnewyork.us/api/v3/views/e5aq-a4j2/query.json"
DEFAULT_PAGE_SIZE = 1000


class DobSafetyError(RuntimeError):
    """Raised when DOB Now Safety data cannot be retrieved."""


def _soql_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _clean(value: Any) -> str:
    return str(value or "").strip()


def build_dob_safety_query(search_type: str, values: dict[str, Any]) -> str:
    if search_type == "address":
        house_number = _clean(values.get("house_number"))
        street_name = _clean(values.get("street_name")).upper()
        borough = _clean(values.get("borough")).upper()

        clauses = [
            f"house_number = {_soql_string(house_number)}",
            f"upper(`street_name`) LIKE {_soql_string(f'%{street_name}%')}",
        ]
        if borough:
            clauses.append(f"borough = {_soql_string(borough)}")
        return "SELECT * WHERE " + " AND ".join(clauses)

    if search_type == "device":
        device_number = _clean(values.get("device_number")).upper()
        return f"SELECT * WHERE device_number = {_soql_string(device_number)}"

    if search_type == "bin":
        bin_number = _clean(values.get("bin"))
        return f"SELECT * WHERE bin = {_soql_string(bin_number)}"

    raise ValueError(f"Unsupported DOB Safety search type: {search_type}")


async def search_dob_safety(search_type: str, values: dict[str, Any]) -> list[dict[str, Any]]:
    import aiohttp

    query = build_dob_safety_query(search_type, values)
    headers = {"content-type": "application/json"}
    if settings.nys_app_token:
        headers["x-app-token"] = settings.nys_app_token

    payload = {
        "query": query,
        "page": {"pageNumber": 1, "pageSize": DEFAULT_PAGE_SIZE},
    }

    try:
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(DOB_SAFETY_URL, headers=headers, json=payload) as response:
                if response.status >= 400:
                    raise DobSafetyError(f"DOB Now Safety returned HTTP {response.status}.")
                data = await response.json()
    except aiohttp.ClientError as exc:
        raise DobSafetyError("DOB Now Safety request failed.") from exc
    except ValueError as exc:
        raise DobSafetyError("DOB Now Safety returned an invalid response.") from exc

    if not isinstance(data, list):
        raise DobSafetyError("DOB Now Safety returned an unexpected response shape.")

    rows = [row for row in data if isinstance(row, dict)]
    return sorted(rows, key=lambda row: str(row.get(":updated_at", "")), reverse=True)
