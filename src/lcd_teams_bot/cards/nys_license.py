from __future__ import annotations

from datetime import datetime
from typing import Any

INDIVIDUAL_LICENSE_TYPES = (
    "ALL",
    "Elevator Mechanic License (SH132)",
    "Elevator Inspector License (SH132)",
    "Elevator Accessibility Technician License (SH132)",
    "SH132: Elevator Accessibility Lift Technician",
)

BUSINESS_LICENSE_TYPES = (
    "ALL",
    "Elevator Contractor License (SH131)",
    "Elevator Inspection Contractor License (SH131)",
)

INDIVIDUAL_TYPE_LABELS = {
    "Elevator Mechanic License (SH132)": "Mechanic",
    "Elevator Inspector License (SH132)": "Inspector",
    "Elevator Accessibility Technician License (SH132)": "Acc. Technician",
    "SH132: Elevator Accessibility Lift Technician": "Acc. Lift Technician",
}

BUSINESS_TYPE_LABELS = {
    "Elevator Inspection Contractor License (SH131)": "Elev. Inspector",
    "Elevator Contractor License (SH131)": "Elev. Contractor",
}


def _base_card(body: list[dict[str, Any]], actions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.5",
        "body": body,
        "actions": actions,
    }


def _heading(text: str) -> dict[str, Any]:
    return {
        "type": "TextBlock",
        "text": text,
        "weight": "Bolder",
        "size": "Medium",
        "wrap": True,
    }


def _divider() -> dict[str, Any]:
    return {"type": "TextBlock", "text": "---", "wrap": True}


def _choice_set(field_id: str, label: str, choices: tuple[str, ...]) -> dict[str, Any]:
    return {
        "type": "Input.ChoiceSet",
        "id": field_id,
        "label": label,
        "style": "compact",
        "choices": [{"title": choice, "value": choice} for choice in choices],
    }


def _text_input(
    field_id: str,
    label: str,
    *,
    is_required: bool = False,
    error_message: str | None = None,
) -> dict[str, Any]:
    field: dict[str, Any] = {"type": "Input.Text", "id": field_id, "label": label}
    if is_required:
        field["isRequired"] = True
        field["errorMessage"] = error_message or f"Enter {label.rstrip(':')}."
    return field


def nys_license_start_card() -> dict[str, Any]:
    return _base_card(
        [
            _heading("NYS Elevator License Lookup"),
            {
                "type": "TextBlock",
                "text": "`/nyslic` - Look up NYS Elevator Licensing (Individual & Business).",
                "wrap": True,
            },
            {
                "type": "Input.ChoiceSet",
                "id": "license_kind",
                "label": "Search for",
                "style": "expanded",
                "isRequired": True,
                "errorMessage": "Choose Individual or Business License.",
                "choices": [
                    {"title": "Individual License", "value": "individual"},
                    {"title": "Business License", "value": "business"},
                ],
            },
        ],
        [
            {"type": "Action.Submit", "title": "Next", "data": {"command": "nyslic.choose"}},
            {"type": "Action.Submit", "title": "Cancel", "data": {"command": "nyslic.cancel"}},
        ],
    )


def nys_individual_license_search_card() -> dict[str, Any]:
    return _base_card(
        [
            _heading("NYS Individual Elevator License Lookup"),
            _divider(),
            _choice_set("license_type", "(OPTIONAL) License Type:", INDIVIDUAL_LICENSE_TYPES),
            _text_input(
                "last_name",
                "Last Name (Required):",
                is_required=True,
                error_message="Enter a last name.",
            ),
            _text_input("first_name", "First Name (Optional):"),
            _text_input("license_number", "License Number (Optional):"),
        ],
        [
            {
                "type": "Action.Submit",
                "title": "Search",
                "data": {"command": "nyslic.submit", "license_kind": "individual"},
            },
            {"type": "Action.Submit", "title": "Cancel", "data": {"command": "nyslic.cancel"}},
        ],
    )


def nys_business_license_search_card() -> dict[str, Any]:
    return _base_card(
        [
            _heading("NYS Business Elevator License Lookup"),
            {
                "type": "TextBlock",
                "text": (
                    "_All fields are optional, but you must enter at least ONE search term "
                    "in order for the search to send._"
                ),
                "wrap": True,
            },
            _divider(),
            _choice_set("license_type", "(OPTIONAL) License Type:", BUSINESS_LICENSE_TYPES),
            _text_input("business_name", "Business Name:"),
            _text_input("city", "City:"),
            _text_input("zip_code", "ZIP:"),
            _text_input("license_number", "License Number:"),
        ],
        [
            {
                "type": "Action.Submit",
                "title": "Search",
                "data": {"command": "nyslic.submit", "license_kind": "business"},
            },
            {"type": "Action.Submit", "title": "Cancel", "data": {"command": "nyslic.cancel"}},
        ],
    )


def _format_date(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return "N/A"
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return text
    return parsed.strftime("%m/%d/%Y")


def _value(row: dict[str, Any], key: str) -> str:
    return str(row.get(key) or "N/A")


def _text_cell(text: str, *, bold: bool = False) -> dict[str, Any]:
    item: dict[str, Any] = {"type": "TextBlock", "text": text, "wrap": True}
    if bold:
        item["weight"] = "Bolder"
    return {"type": "TableCell", "items": [item]}


def _individual_type(row: dict[str, Any]) -> str:
    license_type = _value(row, "license_type")
    return INDIVIDUAL_TYPE_LABELS.get(license_type, license_type)


def _business_type(row: dict[str, Any]) -> str:
    license_type = _value(row, "license_type")
    return BUSINESS_TYPE_LABELS.get(license_type, license_type)


def _individual_result_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "TableRow",
        "cells": [
            _text_cell(f"{_value(row, 'first_name')} {_value(row, 'last_name')}".strip()),
            _text_cell(_value(row, "license_number")),
            _text_cell(_value(row, "license_status")),
            _text_cell(_format_date(row.get("issued_date"))),
            _text_cell(_format_date(row.get("expiration_date"))),
            _text_cell(_individual_type(row)),
        ],
    }


def _business_address(row: dict[str, Any]) -> str:
    lines = [_value(row, "address")]
    address_2 = str(row.get("address_2") or "").strip()
    if address_2:
        lines.append(address_2)
    lines.append(
        f"{_value(row, 'city')}, {_value(row, 'state')} {_value(row, 'zip_code')}"
    )
    return "\n".join(lines)


def _business_result_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "TableRow",
        "cells": [
            _text_cell(_value(row, "business_name")),
            _text_cell(_value(row, "license_number")),
            _text_cell(_value(row, "license_status")),
            _text_cell(_format_date(row.get("issued_date"))),
            _text_cell(_format_date(row.get("expiration_date"))),
            _text_cell(_business_type(row)),
            _text_cell(_value(row, "phone")),
            _text_cell(_business_address(row)),
        ],
    }


def nys_individual_license_results_card(rows: list[dict[str, Any]]) -> dict[str, Any]:
    body: list[dict[str, Any]] = [
        _heading(f"Found {len(rows)} Licenses"),
        _divider(),
    ]

    if not rows:
        body.append(
            {"type": "TextBlock", "text": "No matching NYS licenses were found.", "wrap": True}
        )
        return _base_card(body, [])

    visible_rows = rows[:10]
    body.append(
        {
            "type": "Table",
            "firstRowAsHeaders": True,
            "columns": [{"width": 1} for _ in range(6)],
            "rows": [
                {
                    "type": "TableRow",
                    "cells": [
                        _text_cell("Name", bold=True),
                        _text_cell("License No", bold=True),
                        _text_cell("Status", bold=True),
                        _text_cell("Issue", bold=True),
                        _text_cell("Expiration", bold=True),
                        _text_cell("Type", bold=True),
                    ],
                },
                *(_individual_result_row(row) for row in visible_rows),
            ],
        }
    )
    if len(rows) > len(visible_rows):
        body.append(
            {
                "type": "TextBlock",
                "text": f"Showing 10 of {len(rows)} matching records.",
                "wrap": True,
                "isSubtle": True,
            }
        )
    return _base_card(body, [])


def nys_business_license_results_card(rows: list[dict[str, Any]]) -> dict[str, Any]:
    body: list[dict[str, Any]] = [
        _heading(f"Found {len(rows)} Licenses"),
        _divider(),
    ]

    if not rows:
        body.append(
            {"type": "TextBlock", "text": "No matching NYS licenses were found.", "wrap": True}
        )
        return _base_card(body, [])

    visible_rows = rows[:10]
    body.append(
        {
            "type": "Table",
            "firstRowAsHeaders": True,
            "columns": [{"width": 1} for _ in range(8)],
            "rows": [
                {
                    "type": "TableRow",
                    "cells": [
                        _text_cell("Name", bold=True),
                        _text_cell("License No", bold=True),
                        _text_cell("Status", bold=True),
                        _text_cell("Issue", bold=True),
                        _text_cell("Expiration", bold=True),
                        _text_cell("Type", bold=True),
                        _text_cell("Phone", bold=True),
                        _text_cell("Address", bold=True),
                    ],
                },
                *(_business_result_row(row) for row in visible_rows),
            ],
        }
    )
    if len(rows) > len(visible_rows):
        body.append(
            {
                "type": "TextBlock",
                "text": f"Showing 10 of {len(rows)} matching records.",
                "wrap": True,
                "isSubtle": True,
            }
        )
    return _base_card(body, [])
