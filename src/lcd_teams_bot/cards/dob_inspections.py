from __future__ import annotations

from datetime import datetime
from typing import Any

BOROUGH_CHOICES = (
    "MANHATTAN",
    "BRONX",
    "BROOKLYN",
    "QUEENS",
    "STATEN ISLAND",
)


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


def dob_inspections_start_card() -> dict[str, Any]:
    return _base_card(
        [
            _heading("DOB Inspections"),
            {
                "type": "TextBlock",
                "text": "`/dobinsp` - Look up the most recent filed tests on DOB Now: Safety.",
                "wrap": True,
            },
            {
                "type": "Input.ChoiceSet",
                "id": "search_type",
                "label": "Search by",
                "style": "expanded",
                "isRequired": True,
                "errorMessage": "Choose how you want to search.",
                "choices": [
                    {"title": "Address", "value": "address"},
                    {"title": "Device Number", "value": "device"},
                    {"title": "BIN", "value": "bin"},
                ],
            },
        ],
        [
            {"type": "Action.Submit", "title": "Next", "data": {"command": "dobinsp.choose"}},
            {"type": "Action.Submit", "title": "Cancel", "data": {"command": "dobinsp.cancel"}},
        ],
    )


def dob_inspections_search_card(search_type: str) -> dict[str, Any]:
    if search_type == "address":
        body = [
            _heading("DOB Inspections - Search by Address"),
            {"type": "TextBlock", "text": "---", "wrap": True},
            {
                "type": "Input.ChoiceSet",
                "id": "borough",
                "label": "(OPTIONAL) Select a Boro:",
                "style": "compact",
                "choices": [{"title": boro, "value": boro} for boro in BOROUGH_CHOICES],
            },
            {
                "type": "Input.Text",
                "id": "house_number",
                "label": "House Number:",
                "isRequired": True,
                "errorMessage": "Enter a house number.",
            },
            {
                "type": "Input.Text",
                "id": "street_name",
                "label": "Street Name:",
                "isRequired": True,
                "errorMessage": "Enter a street name.",
            },
            {
                "type": "TextBlock",
                "text": (
                    "_For the street name, enter a part of the street name to search by to "
                    "ensure results are found. Examples include 'East 2' or 'Ditmars' instead "
                    "of 'Ditmars Blvd' and so on._"
                ),
                "wrap": True,
                "isSubtle": True,
            },
        ]
    elif search_type == "device":
        body = [
            _heading("DOB Inspections - Search by Device"),
            {"type": "TextBlock", "text": "---", "wrap": True},
            {
                "type": "Input.Text",
                "id": "device_number",
                "label": "Device Number:",
                "isRequired": True,
                "errorMessage": "Enter a device number.",
            },
        ]
    elif search_type == "bin":
        body = [
            _heading("DOB Inspections - Search by BIN"),
            {"type": "TextBlock", "text": "---", "wrap": True},
            {
                "type": "Input.Text",
                "id": "bin",
                "label": "BIN:",
                "isRequired": True,
                "errorMessage": "Enter a BIN.",
            },
        ]
    else:
        body = [
            _heading("DOB Inspections"),
            {"type": "TextBlock", "text": "Choose a search type.", "wrap": True},
        ]

    return _base_card(
        body,
        [
            {
                "type": "Action.Submit",
                "title": "Search",
                "data": {"command": "dobinsp.submit", "search_type": search_type},
            },
            {"type": "Action.Submit", "title": "Cancel", "data": {"command": "dobinsp.cancel"}},
        ],
    )


def _format_datetime(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return "N/A"
    normalized = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return text
    return parsed.strftime("%m/%d/%Y %H:%M:%S")


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


def _result_container(row: dict[str, Any]) -> dict[str, Any]:
    address = (
        f"{_value(row, 'house_number')} {_value(row, 'street_name')} "
        f"({_value(row, 'borough')}) - {_value(row, 'device_number')}"
    )
    return {
        "type": "Container",
        "separator": True,
        "spacing": "Medium",
        "items": [
            {"type": "TextBlock", "text": f"**{address}**", "wrap": True},
            {
                "type": "TextBlock",
                "text": f"_Last Updated: {_format_datetime(row.get(':updated_at'))}_",
                "wrap": True,
                "isSubtle": True,
            },
            {"type": "TextBlock", "text": "**CAT1 & 5**", "wrap": True, "spacing": "Medium"},
            {
                "type": "TextBlock",
                "text": (
                    f"- **Latest Year Filed:** {_value(row, 'cat1_report_year')}\n"
                    f"- **Last CAT1 Filed:** {_format_date(row.get('cat1_latest_report_filed'))}\n"
                    f"- **Last CAT5 Filed:** {_format_date(row.get('cat5_latest_report_filed'))}"
                ),
                "wrap": True,
            },
            {"type": "TextBlock", "text": "**Periodic**", "wrap": True, "spacing": "Medium"},
            {
                "type": "TextBlock",
                "text": (
                    f"- **Latest Year Filed:** {_value(row, 'periodic_report_year')}\n"
                    f"- **Last Periodic Filed:** {_format_date(row.get('periodic_latest_inspection'))}"
                ),
                "wrap": True,
            },
        ],
    }


def dob_inspections_results_card(rows: list[dict[str, Any]]) -> dict[str, Any]:
    body: list[dict[str, Any]] = [_heading("DOB Now Inspection Results For")]
    if not rows:
        body.append(
            {
                "type": "TextBlock",
                "text": "No matching DOB Now Safety records were found.",
                "wrap": True,
            }
        )
    else:
        visible_rows = rows[:10]
        body.extend(_result_container(row) for row in visible_rows)
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
