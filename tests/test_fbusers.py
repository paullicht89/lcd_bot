import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from lcd_teams_bot.cards.fbusers import fbusers_results_card, fbusers_search_card
from lcd_teams_bot.commands.registry import dispatch_card_action, dispatch_text_command
from lcd_teams_bot.services.dataverse import DataverseError, build_user_params, search_dataverse_users

SERVICE = "lcd_teams_bot.services.dataverse"
REGISTRY = "lcd_teams_bot.commands.registry"
BASE = "https://example.crm.dynamics.com"
ENDPOINT = BASE + "/api/data/v9.2/systemusers"


def config(**overrides):
    values = dict(dataverse_url=BASE, dataverse_access_token="test-token",
                  dataverse_tenant_id="test-tenant", dataverse_client_id="test-client",
                  dataverse_client_secret="test-secret")
    return SimpleNamespace(**(values | overrides))


def response(payload, status=200):
    result = AsyncMock()
    result.status = status
    result.json.return_value = payload
    result.__aenter__.return_value = result
    return result


def session_for(*responses):
    session = AsyncMock()
    session.__aenter__.return_value = session
    session.get = MagicMock(side_effect=responses)
    session.post = MagicMock(return_value=response({"access_token": "fresh-token"}))
    return session


@pytest.mark.parametrize("values,expected", [
    ({"last_name": " Lic "}, "contains(firstname,'') and contains(lastname,'Lic')"),
    ({"first_name": "Ric"}, "contains(firstname,'Ric') and contains(lastname,'')"),
    ({"first_name": "Ric", "last_name": "O'Brien"}, "contains(firstname,'Ric') and contains(lastname,'O''Brien')"),
    ({"last_name": "x') or true or ('"}, "contains(firstname,'') and contains(lastname,'x'') or true or (''')"),
])
def test_filters(values, expected):
    params = build_user_params(values)
    assert params["$select"] == "fullname,systemuserid,domainname"
    assert params["$filter"] == expected + " and contains(domainname,'@lcdelevator.')"


@pytest.mark.parametrize("values", [{}, {"first_name": " "}, {"last_name": []},
                                    {"first_name": 0}, {"last_name": "a" * 101}])
def test_invalid_input_does_not_request(values):
    with patch(f"{SERVICE}.aiohttp.ClientSession") as session:
        with pytest.raises(ValueError):
            asyncio.run(search_dataverse_users(values))
    session.assert_not_called()


def test_get_headers_parameters_and_pagination():
    next_link = ENDPOINT + "?$skiptoken=opaque%26token"
    rows = [{"fullname": "Test Person", "domainname": "test@example.com", "systemuserid": "test-guid"}]
    session = session_for(response({"value": rows, "@odata.nextLink": next_link}),
                          response({"value": [{"fullname": "Second Person"}]}))
    with patch(f"{SERVICE}.settings", config()), patch(f"{SERVICE}.aiohttp.ClientSession", return_value=session):
        assert len(asyncio.run(search_dataverse_users({"last_name": "Person"}))) == 2
    first, second = session.get.call_args_list
    assert first.args == (ENDPOINT,)
    assert first.kwargs["params"] == build_user_params({"last_name": "Person"})
    assert first.kwargs["headers"]["Authorization"] == "Bearer test-token"
    assert first.kwargs["headers"]["Prefer"] == 'odata.include-annotations="OData.Community.Display.V1.FormattedValue"'
    assert first.kwargs["allow_redirects"] is False
    assert second.args == (next_link,)
    assert second.kwargs["params"] is None
    session.post.assert_not_called()


def test_client_credentials_authentication():
    session = session_for(response({"value": []}))
    with patch(f"{SERVICE}.settings", config(dataverse_access_token="")), patch(
        f"{SERVICE}.aiohttp.ClientSession", return_value=session
    ):
        assert asyncio.run(search_dataverse_users({"last_name": "Person"})) == []
    assert session.post.call_args.args == ("https://login.microsoftonline.com/test-tenant/oauth2/v2.0/token",)
    assert session.post.call_args.kwargs["data"] == {
        "client_id": "test-client", "client_secret": "test-secret",
        "grant_type": "client_credentials", "scope": BASE + "/.default",
    }
    assert session.get.call_args.kwargs["headers"]["Authorization"] == "Bearer fresh-token"


@pytest.mark.parametrize("payload,status", [({}, 401), ({}, 403), ({}, 429), ({}, 500),
                                          ({}, 302), ([], 200), ({}, 200), ({"value": [None]}, 200)])
def test_api_errors(payload, status):
    session = session_for(response(payload, status))
    with patch(f"{SERVICE}.settings", config()), patch(f"{SERVICE}.aiohttp.ClientSession", return_value=session):
        with pytest.raises(DataverseError):
            asyncio.run(search_dataverse_users({"last_name": "Person"}))


@pytest.mark.parametrize("next_link", ["https://other.example/api/data/v9.2/systemusers", ENDPOINT,
                                       BASE + "/other", 123])
def test_invalid_continuation_not_requested(next_link):
    session = session_for(response({"value": [], "@odata.nextLink": next_link}))
    with patch(f"{SERVICE}.settings", config()), patch(f"{SERVICE}.aiohttp.ClientSession", return_value=session):
        with pytest.raises(DataverseError):
            asyncio.run(search_dataverse_users({"last_name": "Person"}))
    assert session.get.call_count == 1


@pytest.mark.parametrize("error", [aiohttp.ClientError(), TimeoutError(), ValueError()])
def test_transport_errors(error):
    session = session_for()
    session.__aenter__.side_effect = error
    with patch(f"{SERVICE}.settings", config()), patch(f"{SERVICE}.aiohttp.ClientSession", return_value=session):
        with pytest.raises(DataverseError):
            asyncio.run(search_dataverse_users({"last_name": "Person"}))


@pytest.mark.parametrize("payload,status", [({}, 401), ({}, 200), ({"access_token": 123}, 200)])
def test_authentication_failures(payload, status):
    session = session_for()
    session.post.return_value = response(payload, status)
    with patch(f"{SERVICE}.settings", config(dataverse_access_token="")), patch(
        f"{SERVICE}.aiohttp.ClientSession", return_value=session
    ):
        with pytest.raises(DataverseError):
            asyncio.run(search_dataverse_users({"last_name": "Person"}))
    session.get.assert_not_called()


def test_cards_command_retry_and_cancel():
    context = SimpleNamespace(send_activity=AsyncMock())
    asyncio.run(dispatch_text_command(context, "/fbusers"))
    assert context.send_activity.call_args.args[0].attachments[0].content == fbusers_search_card()
    assert [item["label"] for item in fbusers_search_card()["body"] if item["type"] == "Input.Text"] == ["First Name", "Last Name"]
    empty = fbusers_results_card([])
    assert "Nothing found with that criteria" in empty["body"][1]["text"]
    asyncio.run(dispatch_card_action(context, empty["actions"][0]["data"]))
    assert context.send_activity.call_args.args[0].attachments[0].content == fbusers_search_card()
    with patch(f"{REGISTRY}.search_dataverse_users", new_callable=AsyncMock) as search:
        asyncio.run(dispatch_card_action(context, {"command": "fbusers.cancel"}))
    search.assert_not_awaited()


@pytest.mark.parametrize("count", [0, 1, 23])
def test_results_table_and_batching(count):
    context = SimpleNamespace(send_activity=AsyncMock())
    rows = [{"fullname": f"Person {i}", "domainname": "person@example.com", "systemuserid": f"guid-{i}"} for i in range(count)]
    with patch(f"{REGISTRY}.search_dataverse_users", new_callable=AsyncMock, return_value=rows):
        asyncio.run(dispatch_card_action(context, {"command": "fbusers.submit", "last_name": "Person"}))
    cards = [call.args[0].attachments[0].content for call in context.send_activity.call_args_list]
    tables = [item for card in cards for item in card["body"] if item["type"] == "Table"]
    assert len(cards) == max(1, (count + 9) // 10)
    rendered = []
    for table in tables:
        assert [cell["items"][0]["text"] for cell in table["rows"][0]["cells"]] == ["User's Name", "M365 Email", "FB User GUID"]
        rendered.extend([[cell["items"][0]["text"] for cell in row["cells"]] for row in table["rows"][1:]])
    assert rendered == [[row[key] for key in ("fullname", "domainname", "systemuserid")] for row in rows]


@pytest.mark.parametrize("error", [ValueError("Please enter a name."), DataverseError("private upstream details")])
def test_retryable_errors(error):
    context = SimpleNamespace(send_activity=AsyncMock())
    with patch(f"{REGISTRY}.search_dataverse_users", new_callable=AsyncMock, side_effect=error):
        asyncio.run(dispatch_card_action(context, {"command": "fbusers.submit"}))
    card = context.send_activity.call_args.args[0].attachments[0].content
    assert "private upstream details" not in str(card)
    assert card["actions"][0]["data"]["command"] == "fbusers.submit"
