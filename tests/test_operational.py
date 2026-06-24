from botbuilder.schema import Activity, ChannelAccount, ConversationAccount

from lcd_teams_bot.operational import activity_log_context


def test_activity_log_context_omits_message_text_and_card_values() -> None:
    activity = Activity(
        id="activity-1",
        type="message",
        channel_id="msteams",
        conversation=ConversationAccount(id="conversation-1"),
        from_property=ChannelAccount(id="user-1"),
        text="do not log this",
        value={"secret": "do not log this either"},
    )

    context = activity_log_context(activity)

    assert context == {
        "activity_id": "activity-1",
        "activity_type": "message",
        "channel_id": "msteams",
        "conversation_id": "conversation-1",
        "user_id": "user-1",
    }
