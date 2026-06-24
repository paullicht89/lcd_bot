from __future__ import annotations

import logging

from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity, ActivityTypes
from fastapi import FastAPI, Request, Response
from starlette.responses import JSONResponse

from lcd_teams_bot.commands.registry import dispatch_card_action, dispatch_text_command
from lcd_teams_bot.config import settings
from lcd_teams_bot.operational import activity_log_context, configure_logging

configure_logging(settings.log_level)
log = logging.getLogger("lcd-teams-bot")

adapter_settings = BotFrameworkAdapterSettings(
    app_id=settings.microsoft_app_id,
    app_password=settings.microsoft_app_password,
)
if settings.microsoft_app_tenant_id:
    adapter_settings.channel_auth_tenant = settings.microsoft_app_tenant_id

adapter = BotFrameworkAdapter(adapter_settings)
app = FastAPI(title="LCD Teams Bot")


async def on_turn_error(turn_context: TurnContext, error: Exception) -> None:
    log.error(
        "Unhandled bot turn error",
        extra=activity_log_context(turn_context.activity),
        exc_info=(type(error), error, error.__traceback__),
    )
    await turn_context.send_activity(
        "Sorry, something went wrong while handling that request. The error has been logged."
    )


adapter.on_turn_error = on_turn_error


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.get("/privacy")
async def privacy() -> dict[str, str]:
    return {
        "name": "LCD Teams Bot Privacy",
        "summary": "This internal bot processes Teams messages and command inputs needed to complete requested LCD Elevator workflows.",
    }


@app.get("/terms")
async def terms() -> dict[str, str]:
    return {
        "name": "LCD Teams Bot Terms",
        "summary": "Internal LCD Elevator use only. Users are responsible for submitting accurate command inputs.",
    }


@app.post("/api/messages")
async def messages(request: Request) -> Response:
    try:
        body = await request.json()
        activity = Activity().deserialize(body)
        auth_header = request.headers.get("Authorization", "")
    except Exception:
        log.exception("Invalid Bot Framework request")
        return JSONResponse({"error": "invalid request"}, status_code=400)

    async def turn_handler(turn_context: TurnContext) -> None:
        log.info(
            "Handling bot activity",
            extra=activity_log_context(turn_context.activity),
        )

        if turn_context.activity.type == ActivityTypes.message:
            value = turn_context.activity.value
            if isinstance(value, dict) and value:
                await dispatch_card_action(turn_context, value)
            else:
                await dispatch_text_command(turn_context, turn_context.activity.text)
            return

        if turn_context.activity.type == ActivityTypes.conversation_update:
            await turn_context.send_activity("Hi, I am the LCD Teams Bot. Send `help` to begin.")

    try:
        await adapter.process_activity(activity, auth_header, turn_handler)
        return Response(status_code=201)
    except Exception:
        log.exception("Bot Framework activity processing failed", extra=activity_log_context(activity))
        return JSONResponse({"error": "activity processing failed"}, status_code=500)


def main() -> None:
    import uvicorn

    uvicorn.run(
        "lcd_teams_bot.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "local",
    )


if __name__ == "__main__":
    main()
