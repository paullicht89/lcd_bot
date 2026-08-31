from __future__ import annotations

from typing import Any

from lcd_teams_bot.services.connecteam import custom_field_value


def _base(body: list[dict[str, Any]], actions: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    card: dict[str, Any] = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.5",
        "body": body,
    }
    if actions:
        card["actions"] = actions
    return card


def _heading(text: str) -> dict[str, Any]:
    return {"type": "TextBlock", "text": text, "weight": "Bolder", "size": "Medium", "wrap": True}


def employee_id_search_card() -> dict[str, Any]:
    return _base(
        [
            _heading("Employee ID Number Lookup"),
            {
                "type": "TextBlock",
                "text": "**Please search for the employee's First Name, Last Name, or Phone Number below**",
                "wrap": True,
                "separator": True,
            },
            {"type": "Input.Text", "id": "first_name", "label": "First Name"},
            {"type": "Input.Text", "id": "last_name", "label": "Last Name"},
            {
                "type": "Input.Text",
                "id": "phone_number",
                "label": "Phone Number (No symbols or spaces; e.g. 5165555555)",
                "regex": "^[0-9]{10}$",
                "errorMessage": "Enter a 10-digit phone number without symbols or spaces.",
            },
        ],
        [
            {"type": "Action.Submit", "title": "Search", "data": {"command": "eei.submit"}},
            {"type": "Action.Submit", "title": "Cancel", "data": {"command": "eei.cancel"}},
        ],
    )


def employee_choices_card(users: list[dict[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for user in users:
        name = f"{user.get('firstName', '')} {user.get('lastName', '')}".strip() or "Unnamed user"
        selection = {
            "firstName": user.get("firstName"),
            "lastName": user.get("lastName"),
            "userId": user.get("userId"),
            "customFields": [
                field
                for field in (user.get("customFields") or [])
                if isinstance(field, dict) and field.get("customFieldId") in {9752856, 14375607}
            ],
        }
        rows.append(
            {
                "type": "ColumnSet",
                "separator": bool(rows),
                "columns": [
                    {"type": "Column", "width": "stretch", "items": [{"type": "TextBlock", "text": name, "wrap": True}]},
                    {
                        "type": "Column",
                        "width": "auto",
                        "items": [{
                            "type": "ActionSet",
                            "actions": [{
                                "type": "Action.Submit",
                                "title": "Select User",
                                "data": {"command": "eei.select", "user": selection},
                            }],
                        }],
                    },
                ],
            }
        )
    return _base([_heading("Select an Employee"), *rows])


def employee_id_result_card(user: dict[str, Any]) -> dict[str, Any]:
    name = f"{user.get('firstName', '')} {user.get('lastName', '')}".strip() or "N/A"
    return _base(
        [
            _heading("Showing ID Number(s) for:"),
            {"type": "TextBlock", "text": f"**{name}**", "wrap": True, "separator": True},
            {"type": "FactSet", "separator": True, "facts": [
                {"title": "Connecteam ID:", "value": str(user.get("userId") or "N/A")},
                {"title": "LCD ID:", "value": custom_field_value(user, 9752856)},
                {"title": "HRIS ID:", "value": custom_field_value(user, 14375607)},
            ]},
        ]
    )
