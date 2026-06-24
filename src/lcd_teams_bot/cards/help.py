from __future__ import annotations

from typing import Any, Iterable


def help_card(commands: Iterable[tuple[str, str, tuple[str, ...]]]) -> dict[str, Any]:
    body: list[dict[str, Any]] = [
        {
            "type": "TextBlock",
            "text": "LCD Bot Commands",
            "weight": "Bolder",
            "size": "Medium",
        },
        {
            "type": "TextBlock",
            "text": "Choose one of these commands in chat to start a workflow.",
            "wrap": True,
            "spacing": "Small",
        },
    ]

    for name, description, aliases in commands:
        alias_text = _format_aliases(aliases)
        body.append(
            {
                "type": "Container",
                "spacing": "Medium",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": f"`{name}`{alias_text}",
                        "weight": "Bolder",
                        "wrap": True,
                    },
                    {
                        "type": "TextBlock",
                        "text": description,
                        "wrap": True,
                        "spacing": "None",
                    },
                ],
            }
        )

    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.5",
        "body": body,
    }


def _format_aliases(aliases: tuple[str, ...]) -> str:
    if not aliases:
        return ""
    visible_aliases = ", ".join(f"`{alias}`" for alias in aliases)
    return f" also {visible_aliases}"
