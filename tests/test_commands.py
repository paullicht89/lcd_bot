from lcd_teams_bot.cards.help import help_card
from lcd_teams_bot.commands.registry import COMMAND_BY_NAME, COMMANDS, normalize_command


def test_normalize_command_strips_slash_and_args() -> None:
    assert normalize_command("/lookup 12345") == ("lookup", "12345")


def test_starter_commands_are_registered() -> None:
    for name in ("help", "ping", "status", "lookup", "dobinsp", "ecblookup", "nyslic"):
        assert name in COMMAND_BY_NAME


def test_help_aliases_are_registered() -> None:
    for name in ("help", "cmd", "commands", "menu"):
        assert name in COMMAND_BY_NAME


def test_help_card_lists_registered_commands() -> None:
    card = help_card(
        (command.name, command.description, command.aliases)
        for command in COMMANDS
    )

    assert card["type"] == "AdaptiveCard"
    text_blocks = [
        item["items"][0]["text"]
        for item in card["body"]
        if item.get("type") == "Container"
    ]
    for name in ("help", "ping", "status", "lookup", "dobinsp", "ecblookup", "nyslic"):
        assert any(f"`{name}`" in text for text in text_blocks)
