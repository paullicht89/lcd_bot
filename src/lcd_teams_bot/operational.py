from __future__ import annotations

import logging
import sys
from typing import Any

from botbuilder.schema import Activity


def configure_logging(log_level: str) -> None:
    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stdout,
        force=True,
    )


def activity_log_context(activity: Activity | None) -> dict[str, Any]:
    if activity is None:
        return {}

    channel_id = getattr(activity, "channel_id", None)
    activity_type = getattr(activity, "type", None)
    activity_id = getattr(activity, "id", None)
    conversation = getattr(activity, "conversation", None)
    conversation_id = getattr(conversation, "id", None) if conversation else None
    from_property = getattr(activity, "from_property", None)
    user_id = getattr(from_property, "id", None) if from_property else None

    return {
        "activity_id": activity_id,
        "activity_type": activity_type,
        "channel_id": channel_id,
        "conversation_id": conversation_id,
        "user_id": user_id,
    }
