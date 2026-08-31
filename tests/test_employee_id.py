import pytest

from lcd_teams_bot.cards.employee_id import (
    employee_choices_card,
    employee_id_result_card,
    employee_id_search_card,
)
from lcd_teams_bot.services.connecteam import custom_field_value, normalize_phone


def test_search_card_has_expected_inputs_and_actions() -> None:
    card = employee_id_search_card()
    ids = {item["id"] for item in card["body"] if item["type"] == "Input.Text"}
    assert ids == {"first_name", "last_name", "phone_number"}
    assert [action["data"]["command"] for action in card["actions"]] == ["eei.submit", "eei.cancel"]


def test_phone_normalization() -> None:
    assert normalize_phone("5165555555") == "+15165555555"
    assert normalize_phone("+1 (516) 555-5555") == "+15165555555"
    with pytest.raises(ValueError):
        normalize_phone("516555")


def test_choice_card_adds_select_action_for_each_user() -> None:
    users = [{
        "firstName": "Paul",
        "lastName": "Licht",
        "userId": 42,
        "customFields": [
            {"customFieldId": 9752856, "value": "LCD-1"},
            {"customFieldId": 9751445, "value": "sensitive"},
        ],
    }]
    card = employee_choices_card(users)
    action = card["body"][1]["columns"][1]["items"][0]["actions"][0]
    assert action["data"] == {
        "command": "eei.select",
        "user": {
            "firstName": "Paul",
            "lastName": "Licht",
            "userId": 42,
            "customFields": [{"customFieldId": 9752856, "value": "LCD-1"}],
        },
    }


def test_result_card_shows_all_ids() -> None:
    user = {
        "firstName": "Paul",
        "lastName": "Licht",
        "userId": 5676939,
        "customFields": [
            {"customFieldId": 9752856, "value": "2010002"},
            {"customFieldId": 14375607, "value": "223"},
        ],
    }
    card = employee_id_result_card(user)
    facts = card["body"][2]["facts"]
    assert [(fact["title"], fact["value"]) for fact in facts] == [
        ("Connecteam ID:", "5676939"),
        ("LCD ID:", "2010002"),
        ("HRIS ID:", "223"),
    ]
    assert custom_field_value(user, 999) == "N/A"
