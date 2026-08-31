import asyncio
from unittest.mock import AsyncMock, patch

from lcd_teams_bot.cards.help import help_card
from lcd_teams_bot.commands.registry import COMMAND_BY_NAME, COMMANDS, dispatch_card_action, normalize_command


def test_normalize_command_strips_slash_and_args() -> None:
    assert normalize_command("/lookup 12345") == ("lookup", "12345")


def test_starter_commands_are_registered() -> None:
    for name in (
        "help",
        "ping",
        "status",
        "lookup",
        "dobinsp",
        "ecblookup",
        "nyslic",
        "pwgen",
        "eei",
        "maptiveup",
    ):
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
    for name in (
        "help",
        "ping",
        "status",
        "lookup",
        "dobinsp",
        "ecblookup",
        "nyslic",
        "pwgen",
        "eei",
        "maptiveup",
    ):
        assert any(f"`{name}`" in text for text in text_blocks)


def test_help_card_adds_run_button_for_each_command() -> None:
    card = help_card(
        (command.name, command.description, command.aliases)
        for command in COMMANDS
    )

    containers = [item for item in card["body"] if item.get("type") == "Container"]
    assert len(containers) == len(COMMANDS)

    for command, container in zip(COMMANDS, containers):
        action_set = container["items"][2]
        assert action_set["type"] == "ActionSet"
        assert action_set["actions"] == [
            {
                "type": "Action.Submit",
                "title": f"Run {command.name}",
                "data": {"command": "command.run", "target": command.name},
            }
        ]


def test_command_run_card_action_dispatches_registered_command() -> None:
    class FakeTurnContext:
        def __init__(self) -> None:
            self.messages = []

        async def send_activity(self, activity):
            self.messages.append(activity)

    turn_context = FakeTurnContext()

    asyncio.run(dispatch_card_action(turn_context, {"command": "command.run", "target": "ping"}))

    assert turn_context.messages == ["pong"]


def test_help_card_uses_full_teams_width() -> None:
    card = help_card(
        (command.name, command.description, command.aliases)
        for command in COMMANDS
    )

    assert card["msteams"] == {"width": "Full"}


def test_maptiveup_command_requires_selection_and_confirmation() -> None:
    class FakeTurnContext:
        def __init__(self) -> None:
            self.messages = []

        async def send_activity(self, activity):
            self.messages.append(activity)

    turn_context = FakeTurnContext()
    asyncio.run(dispatch_card_action(turn_context, {"command": "command.run", "target": "maptiveup"}))

    card = turn_context.messages[0].attachments[0].content
    choice_set = next(item for item in card["body"] if item["type"] == "Input.ChoiceSet")
    assert choice_set["choices"] == [
        {"title": "Maptive", "value": "maptive"},
        {"title": "Dataverse", "value": "dataverse"},
    ]
    assert [action["data"] for action in card["actions"]] == [
        {"command": "maptiveup.submit"},
        {"command": "maptiveup.cancel"},
    ]


def test_maptiveup_submit_calls_maptive_webhook_and_reports_success() -> None:
    class FakeTurnContext:
        def __init__(self) -> None:
            self.messages = []

        async def send_activity(self, activity):
            self.messages.append(activity)

    turn_context = FakeTurnContext()
    with patch(
        "lcd_teams_bot.commands.registry.force_maptive_sync", new_callable=AsyncMock
    ) as sync:
        asyncio.run(
            dispatch_card_action(
                turn_context,
                {"command": "maptiveup.submit", "update_target": "maptive"},
            )
        )

    sync.assert_awaited_once()
    assert turn_context.messages == ["Maptive force update: Successful."]


def test_maptiveup_submit_calls_dataverse_webhook_and_reports_success() -> None:
    class FakeTurnContext:
        def __init__(self) -> None:
            self.messages = []

        async def send_activity(self, activity):
            self.messages.append(activity)

    turn_context = FakeTurnContext()
    with patch(
        "lcd_teams_bot.commands.registry.force_dataverse_sync", new_callable=AsyncMock
    ) as sync:
        asyncio.run(
            dispatch_card_action(
                turn_context,
                {"command": "maptiveup.submit", "update_target": "dataverse"},
            )
        )

    sync.assert_awaited_once()
    assert turn_context.messages == ["Dataverse force update: Successful."]
