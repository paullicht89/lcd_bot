import asyncio
from unittest.mock import patch

from lcd_teams_bot.services.maptive import (
    DATAVERSE_SYNC_URL,
    MAPTIVE_SYNC_URL,
    force_dataverse_sync,
    force_maptive_sync,
)


class FakeResponse:
    status = 200
    reason = "OK"

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        return None


class FakeSession:
    def __init__(self) -> None:
        self.post_args = None
        self.post_kwargs = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        return None

    def post(self, *args, **kwargs):
        self.post_args = args
        self.post_kwargs = kwargs
        return FakeResponse()


def test_dataverse_sync_posts_all_scope_with_bearer_token() -> None:
    session = FakeSession()
    with patch("lcd_teams_bot.services.maptive.aiohttp.ClientSession", return_value=session):
        asyncio.run(force_dataverse_sync("dataverse-secret"))

    assert session.post_args == (DATAVERSE_SYNC_URL,)
    assert session.post_kwargs == {
        "headers": {"Authorization": "Bearer dataverse-secret"},
        "json": {"scope": "ALL"},
    }


def test_maptive_sync_posts_all_scope_with_bearer_token() -> None:
    session = FakeSession()
    with patch("lcd_teams_bot.services.maptive.aiohttp.ClientSession", return_value=session):
        asyncio.run(force_maptive_sync("maptive-secret"))

    assert session.post_args == (MAPTIVE_SYNC_URL,)
    assert session.post_kwargs == {
        "headers": {"Authorization": "Bearer maptive-secret"},
        "json": {"scope": "ALL"},
    }
