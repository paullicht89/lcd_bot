from __future__ import annotations

from typing import Any


def password_generated_card(password: str) -> dict[str, Any]:
    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.5",
        "body": [
            {
                "type": "TextBlock",
                "text": "Random Password Generated!",
                "weight": "Bolder",
                "size": "Medium",
                "wrap": True,
            },
            {
                "type": "Container",
                "spacing": "Small",
                "separator": True,
                "items": [],
            },
            {
                "type": "TextBlock",
                "text": "_If necessary, please remember to save this password in NordPass!_",
                "wrap": True,
                "spacing": "Medium",
            },
            {
                "type": "TextBlock",
                "text": f"**PASSWORD:** {password}",
                "wrap": True,
                "spacing": "Medium",
            },
        ],
        "actions": [
            {
                "type": "Action.Submit",
                "title": "Generate Another Password",
                "data": {"command": "pwgen.generate"},
            },
            {
                "type": "Action.Submit",
                "title": "Done",
                "data": {"command": "pwgen.done"},
            },
        ],
    }
