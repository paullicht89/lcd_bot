from __future__ import annotations

from typing import Any

from lcd_teams_bot.config import settings

INDIVIDUAL_LICENSE_URL = "https://data.ny.gov/api/v3/views/cxfs-ya8e/query.json"
BUSINESS_LICENSE_URL = "https://data.ny.gov/api/v3/views/jrac-r9vc/query.json"
DEFAULT_PAGE_SIZE = 1000

LICENSE_KIND_INDIVIDUAL = "individual"
LICENSE_KIND_BUSINESS = "business"


class NysLicenseError(RuntimeError):
    """Raised when NYS license data cannot be retrieved."""


def _soql_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _clean(value: Any) -> str:
    return str(value or "").strip()


def _upper_like_clause(field: str, value: Any) -> str | None:
    text = _clean(value).upper()
    if not text:
        return None
    return f"upper(`{field}`) LIKE {_soql_string(f'%{text}%')}"


def _exact_clause(field: str, value: Any) -> str | None:
    text = _clean(value)
    if not text:
        return None
    return f"`{field}` = {_soql_string(text)}"


def _license_type_clause(value: Any) -> str | None:
    text = _clean(value)
    if not text or text.upper() == "ALL":
        return None
    return f"`license_type` = {_soql_string(text)}"


def build_nys_individual_license_query(values: dict[str, Any]) -> str:
    clauses = [
        clause
        for clause in (
            _license_type_clause(values.get("license_type")),
            _upper_like_clause("last_name", values.get("last_name")),
            _upper_like_clause("first_name", values.get("first_name")),
            _exact_clause("license_number", values.get("license_number")),
        )
        if clause is not None
    ]

    if not _clean(values.get("last_name")):
        raise ValueError("Last name is required.")

    return "SELECT * WHERE " + " AND ".join(clauses)


def build_nys_business_license_query(values: dict[str, Any]) -> str:
    clauses = [
        clause
        for clause in (
            _license_type_clause(values.get("license_type")),
            _upper_like_clause("business_name", values.get("business_name")),
            _upper_like_clause("city", values.get("city")),
            _exact_clause("zip_code", values.get("zip_code")),
            _exact_clause("license_number", values.get("license_number")),
        )
        if clause is not None
    ]

    if not clauses:
        raise ValueError("At least one business search field is required.")

    return "SELECT * WHERE " + " AND ".join(clauses)


async def search_nys_individual_licenses(values: dict[str, Any]) -> list[dict[str, Any]]:
    try:
        query = build_nys_individual_license_query(values)
    except ValueError as exc:
        raise NysLicenseError("NYS individual license search has invalid input.") from exc
    return await _search_nys_licenses(INDIVIDUAL_LICENSE_URL, query)


async def search_nys_business_licenses(values: dict[str, Any]) -> list[dict[str, Any]]:
    try:
        query = build_nys_business_license_query(values)
    except ValueError as exc:
        raise NysLicenseError("NYS business license search has invalid input.") from exc
    return await _search_nys_licenses(BUSINESS_LICENSE_URL, query)


async def _search_nys_licenses(url: str, query: str) -> list[dict[str, Any]]:
    import aiohttp

    headers = {"content-type": "application/json"}
    if settings.nys_app_token:
        headers["x-app-token"] = settings.nys_app_token

    payload = {
        "query": query,
        "page": {"pageNumber": 1, "pageSize": DEFAULT_PAGE_SIZE},
        "includeSynthetic": False,
    }

    try:
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status >= 400:
                    raise NysLicenseError(f"NYS license lookup returned HTTP {response.status}.")
                data = await response.json()
    except aiohttp.ClientError as exc:
        raise NysLicenseError("NYS license lookup request failed.") from exc
    except ValueError as exc:
        raise NysLicenseError("NYS license lookup returned an invalid response.") from exc

    if not isinstance(data, list):
        raise NysLicenseError("NYS license lookup returned an unexpected response shape.")

    return [row for row in data if isinstance(row, dict)]
