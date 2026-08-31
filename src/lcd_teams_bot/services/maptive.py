from __future__ import annotations

import aiohttp


MAPTIVE_SYNC_URL = "https://fb.lcd.nyc/webhooks/maptive/sync"
DATAVERSE_SYNC_URL = "https://fb.lcd.nyc/webhooks/dataverse/sync"


class MaptiveSyncError(RuntimeError):
    """A safe-to-display failure from the Maptive synchronization webhook."""


async def force_maptive_sync(secret: str) -> None:
    if not secret:
        raise MaptiveSyncError("The Maptive sync secret is not configured")

    headers = {"Authorization": f"Bearer {secret}"}
    timeout = aiohttp.ClientTimeout(total=30)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                MAPTIVE_SYNC_URL,
                headers=headers,
                json={"scope": "ALL"},
            ) as response:
                if not 200 <= response.status < 300:
                    raise MaptiveSyncError(
                        f"Fieldboss Automations returned HTTP {response.status} {response.reason}"
                    )
    except MaptiveSyncError:
        raise
    except TimeoutError as exc:
        raise MaptiveSyncError("The Fieldboss Automations request timed out") from exc
    except aiohttp.ClientError as exc:
        raise MaptiveSyncError(f"Could not reach Fieldboss Automations: {exc}") from exc


async def force_dataverse_sync(secret: str) -> None:
    if not secret:
        raise MaptiveSyncError("The Dataverse sync secret is not configured")

    headers = {"Authorization": f"Bearer {secret}"}
    timeout = aiohttp.ClientTimeout(total=30)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                DATAVERSE_SYNC_URL,
                headers=headers,
                json={"scope": "ALL"},
            ) as response:
                if not 200 <= response.status < 300:
                    raise MaptiveSyncError(
                        f"Fieldboss Automations returned HTTP {response.status} {response.reason}"
                    )
    except MaptiveSyncError:
        raise
    except TimeoutError as exc:
        raise MaptiveSyncError("The Fieldboss Automations request timed out") from exc
    except aiohttp.ClientError as exc:
        raise MaptiveSyncError(f"Could not reach Fieldboss Automations: {exc}") from exc
