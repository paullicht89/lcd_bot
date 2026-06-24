from lcd_teams_bot.commands.registry import COMMAND_BY_NAME, normalize_command


def test_normalize_command_strips_slash_and_args() -> None:
    assert normalize_command("/lookup 12345") == ("lookup", "12345")


def test_starter_commands_are_registered() -> None:
    for name in ("help", "ping", "status", "lookup"):
        assert name in COMMAND_BY_NAME
