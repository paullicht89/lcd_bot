from __future__ import annotations

from typing import Any


def _card(body: list[dict[str, Any]], actions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard", "version": "1.5", "body": body, "actions": actions,
    }


def _heading(text: str) -> dict[str, Any]:
    return {"type": "TextBlock", "text": text, "weight": "Bolder",
            "size": "Medium", "wrap": True}


def splashtop_search_card(error: str | None = None) -> dict[str, Any]:
    body = [
        _heading("Get Splashtop Basic Device Info"),
        {"type": "TextBlock", "separator": True, "spacing": "Large", "wrap": True,
         "text": "Please enter one or more of the following details to search for a device in Splashtop:"},
    ]
    if error:
        body.append({"type": "TextBlock", "text": error, "color": "Attention", "wrap": True})
    body.extend([
        {"type": "Input.Text", "id": "id", "label": "ID (OPTIONAL)"},
        {"type": "Input.Text", "id": "host_name", "label": "Host Name (OPTIONAL)"},
    ])
    return _card(body, [
        {"type": "Action.Submit", "title": "SUBMIT", "data": {"command": "splashtoppc.submit"}},
        {"type": "Action.Submit", "title": "CANCEL", "associatedInputs": "none",
         "data": {"command": "splashtoppc.cancel"}},
    ])


def _value(row: dict[str, Any], key: str) -> str:
    value = row.get(key)
    return "N/A" if value is None or value == "" else str(value)


def splashtop_results_card(rows: list[dict[str, Any]]) -> dict[str, Any]:
    body = [_heading("Splashtop Device(s) Found" if rows else "No Devices Found")]
    if not rows:
        body.append({"type": "TextBlock", "text": "Please try your search again", "wrap": True})
    for row in rows:
        status = row.get("online_status")
        online = "Yes" if status is True else "No" if status is False else "N/A"
        facts = [
            {"title": label, "value": _value(row, key)}
            for label, key in (
                ("UUID:", "uuid"), ("ID:", "id"), ("Splashtop Device Name:", "name"),
                ("Device Host Name:", "host_name"), ("Operating System:", "os_product"),
            )
        ]
        facts.extend([
            {"title": "Online?:", "value": f"{online} — Last Online {_value(row, 'last_online')}"},
            {"title": "Logged In User:", "value": _value(row, "os_user")},
        ])
        body.append({"type": "FactSet", "separator": True, "spacing": "Large", "facts": facts})
    return _card(body, [
        {"type": "Action.Submit", "title": "SEARCH AGAIN", "associatedInputs": "none",
         "data": {"command": "command.run", "target": "splashtoppc"}},
    ])
