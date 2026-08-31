from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable

from botbuilder.core import TurnContext
from botbuilder.schema import Activity, ActivityTypes, Attachment

from lcd_teams_bot.cards.dob_inspections import (
    dob_inspections_results_card,
    dob_inspections_search_card,
    dob_inspections_start_card,
)
from lcd_teams_bot.cards.ecb_violations import ecb_lookup_results_card, ecb_lookup_search_card
from lcd_teams_bot.cards.help import help_card
from lcd_teams_bot.cards.employee_id import employee_choices_card, employee_id_result_card, employee_id_search_card
from lcd_teams_bot.cards.lookup import lookup_prompt_card
from lcd_teams_bot.cards.maptive import maptive_sync_confirmation_card
from lcd_teams_bot.cards.nys_license import (
    nys_business_license_results_card,
    nys_business_license_search_card,
    nys_individual_license_results_card,
    nys_individual_license_search_card,
    nys_license_start_card,
)
from lcd_teams_bot.cards.password_generator import password_generated_card
from lcd_teams_bot.config import settings
from lcd_teams_bot.services.password_generator import generate_password
from lcd_teams_bot.services.connecteam import ConnecteamError, search_connecteam_users
from lcd_teams_bot.services.dob_safety import DobSafetyError, search_dob_safety
from lcd_teams_bot.services.ecb_violations import EcbViolationsError, search_ecb_violations
from lcd_teams_bot.services.nys_license import (
    LICENSE_KIND_BUSINESS,
    LICENSE_KIND_INDIVIDUAL,
    NysLicenseError,
    search_nys_business_licenses,
    search_nys_individual_licenses,
)
from lcd_teams_bot.services.maptive import MaptiveSyncError, force_dataverse_sync, force_maptive_sync

CARD_CONTENT_TYPE = "application/vnd.microsoft.card.adaptive"

CommandHandler = Callable[[TurnContext, str], Awaitable[None]]


@dataclass(frozen=True)
class CommandDefinition:
    name: str
    description: str
    handler: CommandHandler
    aliases: tuple[str, ...] = ()


def normalize_command(text: str | None) -> tuple[str, str]:
    raw = (text or "").strip()
    if not raw:
        return "", ""
    first, _, rest = raw.partition(" ")
    return first.lstrip("/").lower(), rest.strip()


async def help_command(turn_context: TurnContext, _: str) -> None:
    commands = (
        (command.name, command.description, command.aliases)
        for command in COMMANDS
    )
    await send_adaptive_card(turn_context, help_card(commands))


async def ping_command(turn_context: TurnContext, _: str) -> None:
    await turn_context.send_activity("pong")


async def status_command(turn_context: TurnContext, _: str) -> None:
    configured = "configured" if settings.microsoft_app_id else "missing MicrosoftAppId"
    await turn_context.send_activity(
        f"LCD Teams Bot is running. Environment: `{settings.environment}`. Bot identity: `{configured}`."
    )


async def lookup_command(turn_context: TurnContext, _: str) -> None:
    attachment = Attachment(content_type=CARD_CONTENT_TYPE, content=lookup_prompt_card())
    await turn_context.send_activity(
        Activity(type=ActivityTypes.message, attachments=[attachment])
    )


async def dobinsp_command(turn_context: TurnContext, _: str) -> None:
    await send_adaptive_card(turn_context, dob_inspections_start_card())


async def ecblookup_command(turn_context: TurnContext, _: str) -> None:
    await send_adaptive_card(turn_context, ecb_lookup_search_card())


async def nyslic_command(turn_context: TurnContext, _: str) -> None:
    await send_adaptive_card(turn_context, nys_license_start_card())


async def pwgen_command(turn_context: TurnContext, _: str) -> None:
    await send_adaptive_card(turn_context, password_generated_card(generate_password()))


async def eei_command(turn_context: TurnContext, _: str) -> None:
    await send_adaptive_card(turn_context, employee_id_search_card())


async def maptiveup_command(turn_context: TurnContext, _: str) -> None:
    await send_adaptive_card(turn_context, maptive_sync_confirmation_card())


async def send_adaptive_card(turn_context: TurnContext, card: dict) -> None:
    attachment = Attachment(content_type=CARD_CONTENT_TYPE, content=card)
    await turn_context.send_activity(Activity(type=ActivityTypes.message, attachments=[attachment]))


COMMANDS: tuple[CommandDefinition, ...] = (
    CommandDefinition(
        "help",
        "Show available commands.",
        help_command,
        aliases=("/help", "cmd", "commands", "/commands", "menu", "/menu"),
    ),
    CommandDefinition("ping", "Verify the bot is reachable.", ping_command, aliases=("/ping",)),
    CommandDefinition("status", "Show service status.", status_command, aliases=("/status",)),
    CommandDefinition("lookup", "Start a guided lookup card.", lookup_command, aliases=("/lookup",)),
    CommandDefinition(
        "dobinsp",
        "Look up the most recent filed tests on DOB Now: Safety.",
        dobinsp_command,
        aliases=("/dobinsp",),
    ),
    CommandDefinition(
        "ecblookup",
        "Look up ECB violations on DOB.",
        ecblookup_command,
        aliases=("/ecblookup",),
    ),
    CommandDefinition(
        "nyslic",
        "Look up NYS Elevator Licensing (Individual & Business).",
        nyslic_command,
        aliases=("/nyslic",),
    ),
    CommandDefinition(
        "pwgen",
        "Generate a random temporary password.",
        pwgen_command,
        aliases=("/pwgen",),
    ),
    CommandDefinition(
        "eei",
        "Look up employee Connecteam, LCD, and HRIS ID numbers.",
        eei_command,
        aliases=("/eei",),
    ),
    CommandDefinition(
        "maptiveup",
        "Force an update of Maptive or Dataverse data from Fieldboss Automations.",
        maptiveup_command,
        aliases=("/maptiveup",),
    ),
)

COMMAND_BY_NAME = {
    name: command
    for command in COMMANDS
    for name in (command.name, *(alias.lstrip("/").lower() for alias in command.aliases))
}


async def dispatch_text_command(turn_context: TurnContext, text: str | None) -> None:
    name, args = normalize_command(text)
    if not name:
        await help_command(turn_context, "")
        return

    command = COMMAND_BY_NAME.get(name)
    if command is None:
        await turn_context.send_activity(f"I do not know `{name}` yet. Try `help`.")
        return

    await command.handler(turn_context, args)


async def dispatch_card_action(turn_context: TurnContext, value: dict) -> None:
    command = str(value.get("command", "")).strip().lower()
    if command == "command.run":
        await dispatch_text_command(turn_context, str(value.get("target", "")))
        return

    if command == "lookup.submit":
        source = value.get("source", "")
        query = value.get("query", "")
        await turn_context.send_activity(
            f"Lookup request received for source `{source}` with query `{query}`. "
            "The integration handler is the next piece to wire in."
        )
        return

    if command == "dobinsp.cancel":
        await turn_context.send_activity("DOB inspection lookup canceled.")
        return

    if command == "dobinsp.choose":
        search_type = str(value.get("search_type", "")).strip().lower()
        if search_type not in {"address", "device", "bin"}:
            await turn_context.send_activity("Choose Address, Device Number, or BIN to continue.")
            return
        await send_adaptive_card(turn_context, dob_inspections_search_card(search_type))
        return

    if command == "dobinsp.submit":
        search_type = str(value.get("search_type", "")).strip().lower()
        if search_type not in {"address", "device", "bin"}:
            await turn_context.send_activity("Choose Address, Device Number, or BIN to continue.")
            return

        missing = _missing_dob_fields(search_type, value)
        if missing:
            await turn_context.send_activity(f"Please provide: {', '.join(missing)}.")
            return

        try:
            rows = await search_dob_safety(search_type, value)
        except DobSafetyError:
            await turn_context.send_activity(
                "Sorry, I could not retrieve DOB Now Safety results right now."
            )
            return

        await send_adaptive_card(turn_context, dob_inspections_results_card(rows))
        return

    if command == "ecblookup.cancel":
        await turn_context.send_activity("ECB violation lookup canceled.")
        return

    if command == "ecblookup.submit":
        if not _has_ecb_filter(value):
            await turn_context.send_activity("Please provide at least one ECB lookup field.")
            return

        try:
            rows = await search_ecb_violations(value)
        except EcbViolationsError:
            await turn_context.send_activity(
                "Sorry, I could not retrieve ECB violation results right now."
            )
            return

        await send_adaptive_card(turn_context, ecb_lookup_results_card(rows))
        return

    if command == "nyslic.cancel":
        await turn_context.send_activity("NYS license lookup canceled.")
        return

    if command == "nyslic.choose":
        license_kind = str(value.get("license_kind", "")).strip().lower()
        if license_kind == LICENSE_KIND_INDIVIDUAL:
            await send_adaptive_card(turn_context, nys_individual_license_search_card())
            return
        if license_kind == LICENSE_KIND_BUSINESS:
            await send_adaptive_card(turn_context, nys_business_license_search_card())
            return
        await turn_context.send_activity("Choose Individual or Business License to continue.")
        return

    if command == "nyslic.submit":
        license_kind = str(value.get("license_kind", "")).strip().lower()

        if license_kind == LICENSE_KIND_INDIVIDUAL:
            if not str(value.get("last_name", "")).strip():
                await turn_context.send_activity("Please provide a last name.")
                return
            try:
                rows = await search_nys_individual_licenses(value)
            except NysLicenseError:
                await turn_context.send_activity(
                    "Sorry, I could not retrieve NYS individual license results right now."
                )
                return
            await send_adaptive_card(turn_context, nys_individual_license_results_card(rows))
            return

        if license_kind == LICENSE_KIND_BUSINESS:
            if not _has_nys_business_filter(value):
                await turn_context.send_activity("Please provide at least one business lookup field.")
                return
            try:
                rows = await search_nys_business_licenses(value)
            except NysLicenseError:
                await turn_context.send_activity(
                    "Sorry, I could not retrieve NYS business license results right now."
                )
                return
            await send_adaptive_card(turn_context, nys_business_license_results_card(rows))
            return

        await turn_context.send_activity("Choose Individual or Business License to continue.")
        return

    if command == "pwgen.generate":
        await send_adaptive_card(turn_context, password_generated_card(generate_password()))
        return

    if command == "pwgen.done":
        await turn_context.send_activity("Password generation done.")
        return

    if command == "eei.cancel":
        await turn_context.send_activity("Employee ID lookup canceled.")
        return

    if command == "eei.submit":
        if not any(str(value.get(key, "")).strip() for key in ("first_name", "last_name", "phone_number")):
            await turn_context.send_activity("Please provide a first name, last name, or phone number.")
            return
        try:
            users = await search_connecteam_users(value)
        except ValueError:
            await turn_context.send_activity("Enter a 10-digit phone number without symbols or spaces.")
            return
        except ConnecteamError:
            await turn_context.send_activity("Sorry, I could not retrieve Connecteam users right now.")
            return
        if not users:
            await turn_context.send_activity("No users matching the name or phone number have been found.")
        elif len(users) == 1:
            await send_adaptive_card(turn_context, employee_id_result_card(users[0]))
        else:
            await send_adaptive_card(turn_context, employee_choices_card(users))
        return

    if command == "eei.select":
        user = value.get("user")
        if not isinstance(user, dict):
            await turn_context.send_activity("That employee selection is invalid. Please run `/eei` again.")
            return
        await send_adaptive_card(turn_context, employee_id_result_card(user))
        return

    if command == "maptiveup.cancel":
        await turn_context.send_activity("Data force update canceled.")
        return

    if command == "maptiveup.submit":
        update_target = str(value.get("update_target", "")).strip().lower()
        if update_target not in {"maptive", "dataverse"}:
            await turn_context.send_activity("Select Maptive or Dataverse before submitting.")
            return

        try:
            if update_target == "maptive":
                await force_maptive_sync(settings.maptive_sync_secret)
            else:
                await force_dataverse_sync(settings.dataverse_sync_secret)
        except MaptiveSyncError as exc:
            await turn_context.send_activity(
                f"{update_target.title()} force update failed: {exc}. "
                "Please forward this error to IT."
            )
            return
        await turn_context.send_activity(f"{update_target.title()} force update: Successful.")
        return

    await turn_context.send_activity("I received the card action, but no handler is registered yet.")


def _missing_dob_fields(search_type: str, value: dict) -> list[str]:
    if search_type == "address":
        required = (("house_number", "House Number"), ("street_name", "Street Name"))
    elif search_type == "device":
        required = (("device_number", "Device Number"),)
    else:
        required = (("bin", "BIN"),)
    return [label for key, label in required if not str(value.get(key, "")).strip()]


def _has_ecb_filter(value: dict) -> bool:
    fields = (
        "ecb_no",
        "bin",
        "ecb_violation_status",
        "hearing_status",
        "severity",
        "certification_status",
    )
    return any(str(value.get(field, "")).strip() for field in fields)


def _has_nys_business_filter(value: dict) -> bool:
    if str(value.get("license_type", "")).strip().upper() not in {"", "ALL"}:
        return True
    fields = ("business_name", "city", "zip_code", "license_number")
    return any(str(value.get(field, "")).strip() for field in fields)
