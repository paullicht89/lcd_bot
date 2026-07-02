import re

from lcd_teams_bot.cards.password_generator import password_generated_card
from lcd_teams_bot.services.password_generator import generate_password


def test_generate_password_uses_expected_format() -> None:
    password = generate_password()

    assert re.fullmatch(r"[A-Z][a-z]+-[A-Z][a-z]+-[A-Z][a-z]+-\d{2}[!#$%?@]", password)


def test_password_generated_card_has_expected_text_and_actions() -> None:
    card = password_generated_card("Leaf-Train-Rock-42!")

    assert card["type"] == "AdaptiveCard"
    text = [item["text"] for item in card["body"] if item["type"] == "TextBlock"]
    assert "Random Password Generated!" in text
    assert "**PASSWORD:** Leaf-Train-Rock-42!" in text
    assert card["actions"][0]["title"] == "Generate Another Password"
    assert card["actions"][0]["data"] == {"command": "pwgen.generate"}
    assert card["actions"][1]["title"] == "Done"
    assert card["actions"][1]["data"] == {"command": "pwgen.done"}
