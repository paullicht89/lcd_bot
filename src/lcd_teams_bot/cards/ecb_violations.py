from __future__ import annotations

from typing import Any

VIOLATION_STATUS_CHOICES = ("ACTIVE", "RESOLVE", "Unknown")
HEARING_STATUS_CHOICES = (
    "ADMIN/IN-VIO",
    "CURED/IN-VIO",
    "DEFAULT",
    "IN VIOLATION",
    "PENDING",
    "POP/IN-VIO",
    "STIPULATION/IN-VIO",
    "WRITTEN OFF",
)
SEVERITY_CHOICES = ("CLASS-1", "CLASS-2", "CLASS-3", "Hazardous", "Non-Hazardous", "Unknown")
CERTIFICATION_STATUS_CHOICES = (
    "CERTIFICATE ACCEPTED",
    "CERTIFICATE DISAPPROVED",
    "CERTIFICATE PENDING",
    "COMPLIANCE-INSP/DOC",
    "CURE ACCEPTED",
    "N/A - DISMISSED",
    "NO COMPLIANCE RECORDED",
    "REINSPECTION SHOWS STILL IN VIOLATION",
    "REINSPECTION SHOWS VIOLATION GOOD",
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


def _choice_set(field_id: str, label: str, choices: tuple[str, ...]) -> dict[str, Any]:
    return {
        "type": "Input.ChoiceSet",
        "id": field_id,
        "label": label,
        "style": "compact",
        "choices": [{"title": choice, "value": choice} for choice in choices],
    }


def ecb_lookup_search_card() -> dict[str, Any]:
    return _base_card(
        [
            _heading("ECB Violation Lookup"),
            {
                "type": "TextBlock",
                "text": (
                    "_Search by one or more of these fields. Note: This lookup CANNOT be "
                    "searched by building or device number!_"
                ),
                "wrap": True,
            },
            {"type": "TextBlock", "text": "---", "wrap": True},
            {"type": "Input.Text", "id": "ecb_no", "label": "ECB Number:"},
            {"type": "Input.Text", "id": "bin", "label": "BIN:"},
            _choice_set("ecb_violation_status", "Violation Status:", VIOLATION_STATUS_CHOICES),
            _choice_set("hearing_status", "Hearing Status:", HEARING_STATUS_CHOICES),
            _choice_set("severity", "Severity:", SEVERITY_CHOICES),
            _choice_set(
                "certification_status",
                "Certification Status:",
                CERTIFICATION_STATUS_CHOICES,
            ),
        ],
        [
            {"type": "Action.Submit", "title": "Search", "data": {"command": "ecblookup.submit"}},
            {"type": "Action.Submit", "title": "Cancel", "data": {"command": "ecblookup.cancel"}},
        ],
    )


def _value(row: dict[str, Any], key: str) -> str:
    return str(row.get(key) or "N/A")


def _ecb_number(row: dict[str, Any]) -> str:
    return _value(row, "ecb_violation_number")


def _open_url_action(title: str, url: str) -> dict[str, Any]:
    return {"type": "Action.OpenUrl", "title": title, "url": url}


def _action_cell(actions: list[dict[str, Any]]) -> dict[str, Any]:
    return {"type": "TableCell", "items": [{"type": "ActionSet", "actions": actions}]}


def _text_cell(text: str, *, bold: bool = False) -> dict[str, Any]:
    item: dict[str, Any] = {"type": "TextBlock", "text": text, "wrap": True}
    if bold:
        item["weight"] = "Bolder"
    return {"type": "TableCell", "items": [item]}


def _result_row(row: dict[str, Any]) -> dict[str, Any]:
    ecb_number = _ecb_number(row)
    return {
        "type": "TableRow",
        "cells": [
            _text_cell(ecb_number),
            _text_cell(_value(row, "ecb_violation_status")),
            _text_cell(_value(row, "severity")),
            _action_cell(
                [
                    {
                        "type": "Action.Submit",
                        "title": "View Details",
                        "isEnabled": False,
                        "data": {"command": "ecblookup.details", "ecb_no": ecb_number},
                    }
                ]
            ),
            _action_cell(
                [
                    _open_url_action(
                        "DOB Link",
                        "https://a810-bisweb.nyc.gov/bisweb/"
                        f"ECBQueryByNumberServlet?requestid=3&ecbin={ecb_number}",
                    )
                ]
            ),
            _action_cell(
                [
                    _open_url_action(
                        "DOB Image",
                        "http://a820-ecbticketfinder.nyc.gov/"
                        f"GetViolationImage?violationNumber=0{ecb_number}",
                    )
                ]
            ),
        ],
    }


def ecb_lookup_results_card(rows: list[dict[str, Any]]) -> dict[str, Any]:
    body: list[dict[str, Any]] = [
        _heading("ECB Lookup Results"),
        {"type": "TextBlock", "text": f"**{len(rows)} ECB Violations Found**", "wrap": True},
        {"type": "TextBlock", "text": "---", "wrap": True},
    ]

    if not rows:
        body.append(
            {"type": "TextBlock", "text": "No matching ECB violations were found.", "wrap": True}
        )
        return _base_card(body, [])

    visible_rows = rows[:10]
    body.append(
        {
            "type": "Table",
            "firstRowAsHeaders": True,
            "columns": [
                {"width": 1},
                {"width": 1},
                {"width": 1},
                {"width": 1},
                {"width": 1},
                {"width": 1},
            ],
            "rows": [
                {
                    "type": "TableRow",
                    "cells": [
                        _text_cell("ECB No.", bold=True),
                        _text_cell("Status", bold=True),
                        _text_cell("Severity", bold=True),
                        _text_cell("View Details", bold=True),
                        _text_cell("DOB Link", bold=True),
                        _text_cell("DOB Image", bold=True),
                    ],
                },
                *(_result_row(row) for row in visible_rows),
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
