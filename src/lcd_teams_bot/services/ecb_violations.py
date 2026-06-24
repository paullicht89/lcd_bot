from __future__ import annotations

from typing import Any

from lcd_teams_bot.config import settings

ECB_VIOLATIONS_URL = "https://data.cityofnewyork.us/api/v3/views/6bgk-3dad/query.json"
DEFAULT_PAGE_SIZE = 1000


class EcbViolationsError(RuntimeError):
    """Raised when ECB violation data cannot be retrieved."""


FIELD_MAP = {
    "ecb_no": "ecb_violation_number",
    "bin": "bin",
    "ecb_violation_status": "ecb_violation_status",
    "hearing_status": "hearing_status",
    "severity": "severity",
    "certification_status": "certification_status",
}

SEVERITY_ALIASES = {
    "CLASS-1": ("CLASS-1", "CLASS - 1"),
    "CLASS-2": ("CLASS-2", "CLASS - 2"),
    "CLASS-3": ("CLASS-3", "CLASS - 3"),
}


def _soql_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _clean(value: Any) -> str:
    return str(value or "").strip()


def _field_clause(field: str, raw_value: Any) -> str | None:
    value = _clean(raw_value)
    if not value:
        return None

    if field == "severity" and value in SEVERITY_ALIASES:
        choices = ", ".join(_soql_string(choice) for choice in SEVERITY_ALIASES[value])
        return f"severity IN ({choices})"

    api_field = FIELD_MAP[field]
    return f"{api_field} = {_soql_string(value)}"


def build_ecb_violations_query(values: dict[str, Any]) -> str:
    clauses = ["violation_type = 'Elevators'"]
    clauses.extend(
        clause
        for field in FIELD_MAP
        if (clause := _field_clause(field, values.get(field))) is not None
    )

    if len(clauses) == 1:
        raise ValueError("At least one ECB search field is required.")

    return "SELECT * WHERE " + " AND ".join(clauses)


async def search_ecb_violations(values: dict[str, Any]) -> list[dict[str, Any]]:
    import aiohttp

    try:
        query = build_ecb_violations_query(values)
    except ValueError as exc:
        raise EcbViolationsError("ECB violation search needs at least one filter.") from exc

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
            async with session.post(ECB_VIOLATIONS_URL, headers=headers, json=payload) as response:
                if response.status >= 400:
                    raise EcbViolationsError(f"ECB violations returned HTTP {response.status}.")
                data = await response.json()
    except aiohttp.ClientError as exc:
        raise EcbViolationsError("ECB violations request failed.") from exc
    except ValueError as exc:
        raise EcbViolationsError("ECB violations returned an invalid response.") from exc

    if not isinstance(data, list):
        raise EcbViolationsError("ECB violations returned an unexpected response shape.")

    rows = [row for row in data if isinstance(row, dict)]
    return sorted(rows, key=lambda row: str(row.get(":updated_at", "")), reverse=True)
