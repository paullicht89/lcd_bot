from __future__ import annotations

from typing import Any


def lookup_prompt_card() -> dict[str, Any]:
    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.5",
        "body": [
            {
                "type": "TextBlock",
                "text": "Lookup",
                "weight": "Bolder",
                "size": "Medium",
            },
            {
                "type": "TextBlock",
                "text": "Choose a source and enter a search value.",
                "wrap": True,
            },
            {
                "type": "Input.ChoiceSet",
                "id": "source",
                "label": "Source",
                "style": "compact",
                "isRequired": True,
                "errorMessage": "Choose a source.",
                "choices": [
                    {"title": "NYC DOB", "value": "nyc_dob"},
                    {"title": "Connecteam", "value": "connecteam"},
                    {"title": "Microsoft Graph", "value": "graph"},
                ],
            },
            {
                "type": "Input.Text",
                "id": "query",
                "label": "Search value",
                "placeholder": "BIN, device number, employee name, email, etc.",
                "isRequired": True,
                "errorMessage": "Enter a search value.",
            },
        ],
        "actions": [
            {
                "type": "Action.Submit",
                "title": "Search",
                "data": {"command": "lookup.submit"},
            }
        ],
    }
