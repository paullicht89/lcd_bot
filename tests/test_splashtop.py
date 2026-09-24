import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from lcd_teams_bot.cards.splashtop import splashtop_results_card, splashtop_search_card
from lcd_teams_bot.commands.registry import dispatch_card_action, dispatch_text_command
from lcd_teams_bot.services.splashtop import (
    SplashtopError, search_splashtop_computers,
)

SERVICE = "lcd_teams_bot.services.splashtop"
REGISTRY = "lcd_teams_bot.commands.registry"


@pytest.mark.parametrize("values,expected", [
    ({"id": " 123 "}, {"ids": "123"}),
    ({"host_name": " PC & Test "}, {"host_name": "PC & Test"}),
    ({"id": "123", "host_name": "PC"}, {"ids": "123", "host_name": "PC"}),
])
def test_lookup_request(values, expected):
    response = AsyncMock()
    response.status = 200
    response.json.return_value = {"result": 20200, "data": [{"id": 123}]}
    session = AsyncMock()
    session.get = MagicMock(return_value=response)
    session.__aenter__.return_value = session
    response.__aenter__.return_value = response
    config = SimpleNamespace(splashtop_team_id="456", splashtop_api_token="test-token")
    with patch(f"{SERVICE}.settings", config), patch(
        f"{SERVICE}.aiohttp.ClientSession", return_value=session
    ):
        assert asyncio.run(search_splashtop_computers(values)) == [{"id": 123}]
    session.get.assert_called_once_with(
        "https://webapi.splashtop.com/api/open/v1/teams/456/computers",
        params=expected, headers={"Authorization": "Bearer test-token"}, allow_redirects=False,
    )


@pytest.mark.parametrize("values", [{}, {"id": " ", "host_name": None},
                                      {"id": "abc"}, {"id": []}, {"id": "１２３"}])
def test_invalid_input_never_opens_session(values):
    with patch(f"{SERVICE}.aiohttp.ClientSession") as session:
        with pytest.raises(ValueError):
            asyncio.run(search_splashtop_computers(values))
    session.assert_not_called()


@pytest.mark.parametrize("status,payload,error", [
    (200, {"result": 20200, "data": []}, None),
    (401, {}, SplashtopError), (429, {}, SplashtopError), (500, {}, SplashtopError),
    (302, {}, SplashtopError), (200, {"result": 40400, "data": []}, SplashtopError),
    (200, [], SplashtopError), (200, {"result": 20200}, SplashtopError),
    (200, {"result": 20200, "data": [None]}, SplashtopError),
])
def test_api_response_validation(status, payload, error):
    response = AsyncMock()
    response.status = status
    response.json.return_value = payload
    response.__aenter__.return_value = response
    session = AsyncMock()
    session.__aenter__.return_value = session
    session.get = MagicMock(return_value=response)
    with patch(f"{SERVICE}.settings", SimpleNamespace(
        splashtop_team_id="456", splashtop_api_token="test-token"
    )), patch(f"{SERVICE}.aiohttp.ClientSession", return_value=session):
        if error:
            with pytest.raises(error):
                asyncio.run(search_splashtop_computers({"id": "123"}))
        else:
            assert asyncio.run(search_splashtop_computers({"id": "123"})) == []


@pytest.mark.parametrize("error", [TimeoutError(), aiohttp.ClientError(), ValueError()])
def test_transport_and_json_failures(error):
    session = AsyncMock()
    session.__aenter__.side_effect = error
    with patch(f"{SERVICE}.settings", SimpleNamespace(
        splashtop_team_id="456", splashtop_api_token="test-token"
    )), patch(f"{SERVICE}.aiohttp.ClientSession", return_value=session):
        with pytest.raises(SplashtopError):
            asyncio.run(search_splashtop_computers({"id": "123"}))


def test_missing_config_never_requests():
    with patch(f"{SERVICE}.settings", SimpleNamespace(
        splashtop_team_id="", splashtop_api_token=""
    )), patch(f"{SERVICE}.aiohttp.ClientSession") as session:
        with pytest.raises(SplashtopError):
            asyncio.run(search_splashtop_computers({"id": "123"}))
    session.assert_not_called()


def test_cards_and_retry_flow():
    context = SimpleNamespace(send_activity=AsyncMock())
    asyncio.run(dispatch_text_command(context, "/splashtoppc"))
    card = context.send_activity.call_args.args[0].attachments[0].content
    assert card == splashtop_search_card()
    assert [(item["id"], item["label"]) for item in card["body"]
            if item["type"] == "Input.Text"] == [
        ("id", "ID (OPTIONAL)"), ("host_name", "Host Name (OPTIONAL)"),
    ]
    assert card["actions"][1]["associatedInputs"] == "none"
    empty = splashtop_results_card([])
    assert empty["body"][0]["text"] == "No Devices Found"
    asyncio.run(dispatch_card_action(context, empty["actions"][0]["data"]))
    assert context.send_activity.call_args.args[0].attachments[0].content == card
    with patch(f"{REGISTRY}.search_splashtop_computers", new_callable=AsyncMock) as lookup:
        asyncio.run(dispatch_card_action(context, card["actions"][1]["data"]))
    lookup.assert_not_awaited()
    assert context.send_activity.call_args.args[0] == "Splashtop device lookup canceled."


def test_result_fields_and_multiple_devices():
    row = {"uuid": "test-uuid", "id": 123, "name": "Test Device", "host_name": "PC",
           "os_product": "Windows", "online_status": False, "last_online": "2026-09-24 12:00:00",
           "os_user": "test-user"}
    card = splashtop_results_card([row, {"id": 124, "online_status": True}])
    facts = {fact["title"]: fact["value"] for fact in card["body"][1]["facts"]}
    assert facts == {"UUID:": "test-uuid", "ID:": "123", "Splashtop Device Name:": "Test Device",
                     "Device Host Name:": "PC", "Operating System:": "Windows",
                     "Online?:": "No — Last Online 2026-09-24 12:00:00", "Logged In User:": "test-user"}
    assert len(card["body"]) == 3


@pytest.mark.parametrize("rows", [[], [{"id": n} for n in range(12)]])
def test_submit_renders_every_device(rows):
    context = SimpleNamespace(send_activity=AsyncMock())
    with patch(f"{REGISTRY}.search_splashtop_computers", new_callable=AsyncMock, return_value=rows):
        asyncio.run(dispatch_card_action(context, {"command": "splashtoppc.submit", "id": "123"}))
    cards = [call.args[0].attachments[0].content for call in context.send_activity.call_args_list]
    assert len(cards) == (3 if rows else 1)
    assert sum(item["type"] == "FactSet" for card in cards for item in card["body"]) == len(rows)


@pytest.mark.parametrize("error", [ValueError("Please enter an ID or Host Name to search."),
                                  SplashtopError("sensitive upstream details")])
def test_submit_errors_are_retryable_and_sanitized(error):
    context = SimpleNamespace(send_activity=AsyncMock())
    with patch(f"{REGISTRY}.search_splashtop_computers", new_callable=AsyncMock, side_effect=error):
        asyncio.run(dispatch_card_action(context, {"command": "splashtoppc.submit"}))
    card = context.send_activity.call_args.args[0].attachments[0].content
    assert "sensitive" not in str(card)
    assert card["actions"][0]["data"]["command"] == "splashtoppc.submit"
