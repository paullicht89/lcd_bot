from __future__ import annotations


def _card(body: list[dict], actions: list[dict]) -> dict:
    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard", "version": "1.5", "msteams": {"width": "Full"},
        "body": body, "actions": actions,
    }


def fbusers_search_card(error: str | None = None) -> dict:
    body = [
        {"type": "TextBlock", "text": "Find Fieldboss Users", "weight": "Bolder", "size": "Medium"},
        {"type": "TextBlock", "text": "Enter a First Name, Last Name, or both. Partial names are supported.", "wrap": True},
    ]
    if error:
        body.append({"type": "TextBlock", "text": error, "wrap": True, "color": "Attention"})
    body.extend([
        {"type": "Input.Text", "id": "first_name", "label": "First Name", "maxLength": 100},
        {"type": "Input.Text", "id": "last_name", "label": "Last Name", "maxLength": 100},
    ])
    return _card(body, [
        {"type": "Action.Submit", "title": "Search", "data": {"command": "fbusers.submit"}},
        {"type": "Action.Submit", "title": "Cancel", "associatedInputs": "none", "data": {"command": "fbusers.cancel"}},
    ])


def _row(values: list[str], *, header: bool = False) -> dict:
    return {"type": "TableRow", "cells": [
        {"type": "TableCell", "items": [{"type": "TextBlock", "text": value, "wrap": True,
                                          "weight": "Bolder" if header else "Default"}]}
        for value in values
    ]}


def fbusers_results_card(rows: list[dict]) -> dict:
    body = [{"type": "TextBlock", "text": "Fieldboss Users" if rows else "No Users Found",
             "weight": "Bolder", "size": "Medium"}]
    if rows:
        body.append({
            "type": "Table", "firstRowAsHeaders": True, "showGridLines": True,
            "columns": [{"width": 1}, {"width": 1}, {"width": 1}],
            "rows": [_row(["User's Name", "M365 Email", "FB User GUID"], header=True),
                     *[_row([str(row.get(key) or "N/A") for key in
                             ("fullname", "domainname", "systemuserid")]) for row in rows]],
        })
    else:
        body.append({"type": "TextBlock", "text": "Nothing found with that criteria. Please try the search again.", "wrap": True})
    return _card(body, [
        {"type": "Action.Submit", "title": "Search Again", "associatedInputs": "none",
         "data": {"command": "command.run", "target": "fbusers"}},
    ])
