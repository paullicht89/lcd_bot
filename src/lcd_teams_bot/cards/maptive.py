from __future__ import annotations

from typing import Any


def maptive_sync_confirmation_card() -> dict[str, Any]:
    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.5",
        "body": [
            {
                "type": "TextBlock",
                "text": "Force Data Update",
                "weight": "Bolder",
                "size": "Medium",
            },
            {
                "type": "TextBlock",
                "text": "Which would you like to update?",
                "wrap": True,
            },
            {
                "type": "Input.ChoiceSet",
                "id": "update_target",
                "style": "expanded",
                "isRequired": True,
                "errorMessage": "Select Maptive or Dataverse.",
                "choices": [
                    {"title": "Maptive", "value": "maptive"},
                    {"title": "Dataverse", "value": "dataverse"},
                ],
            },
        ],
        "actions": [
            {
                "type": "Action.Submit",
                "title": "Submit",
                "style": "positive",
                "data": {"command": "maptiveup.submit"},
            },
            {
                "type": "Action.Submit",
                "title": "Cancel",
                "data": {"command": "maptiveup.cancel"},
            },
        ],
    }
