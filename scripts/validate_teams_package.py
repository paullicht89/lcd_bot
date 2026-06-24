"""Validate the LCD Teams app manifest source or packaged zip."""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
import uuid
import zipfile
from pathlib import Path
from urllib.parse import urlparse


GUID_FIELDS = ("id",)
PLACEHOLDER_RE = re.compile(r"REPLACE-WITH|<[^>]+>", re.IGNORECASE)
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
EXPECTED_ICON_SIZES = {
    "color": (192, 192),
    "outline": (32, 32),
}


class ValidationError(ValueError):
    pass


def read_png_size(data: bytes) -> tuple[int, int]:
    png_header = b"\x89PNG\r\n\x1a\n"
    if not data.startswith(png_header):
        raise ValidationError("is not a PNG file")
    if len(data) < 24:
        raise ValidationError("is too small to contain PNG dimensions")
    return struct.unpack(">II", data[16:24])


def validate_guid(value: str, field_name: str) -> None:
    try:
        uuid.UUID(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field_name} must be a GUID") from exc


def validate_https_url(value: str, field_name: str) -> None:
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValidationError(f"{field_name} must be an https URL")


def validate_no_placeholders(manifest_text: str) -> None:
    match = PLACEHOLDER_RE.search(manifest_text)
    if match:
        raise ValidationError(f"manifest still contains placeholder text: {match.group(0)}")


def validate_manifest(manifest: dict, manifest_text: str) -> None:
    validate_no_placeholders(manifest_text)

    if manifest.get("manifestVersion") != "1.16":
        raise ValidationError("manifestVersion must be 1.16")
    if not SEMVER_RE.match(str(manifest.get("version", ""))):
        raise ValidationError("version must be semantic version format like 0.1.0")

    for field in GUID_FIELDS:
        validate_guid(manifest.get(field, ""), field)

    if len(manifest.get("packageName", "")) > 64:
        raise ValidationError("packageName must be 64 characters or fewer")

    developer = manifest.get("developer", {})
    if len(developer.get("name", "")) > 32:
        raise ValidationError("developer.name must be 32 characters or fewer")
    for field in ("websiteUrl", "privacyUrl", "termsOfUseUrl"):
        validate_https_url(developer.get(field, ""), f"developer.{field}")

    name = manifest.get("name", {})
    if len(name.get("short", "")) > 30:
        raise ValidationError("name.short must be 30 characters or fewer")
    if len(name.get("full", "")) > 100:
        raise ValidationError("name.full must be 100 characters or fewer")

    description = manifest.get("description", {})
    if len(description.get("short", "")) > 80:
        raise ValidationError("description.short must be 80 characters or fewer")
    if len(description.get("full", "")) > 4000:
        raise ValidationError("description.full must be 4000 characters or fewer")

    if not HEX_COLOR_RE.match(str(manifest.get("accentColor", ""))):
        raise ValidationError("accentColor must be a 6-digit hex color like #0B5CAB")

    icons = manifest.get("icons", {})
    for icon_name in EXPECTED_ICON_SIZES:
        icon_path = icons.get(icon_name, "")
        if not icon_path:
            raise ValidationError(f"manifest must reference an {icon_name} icon")
        if icon_path.startswith("/") or ".." in Path(icon_path).parts:
            raise ValidationError(f"manifest icon path must be relative and package-local: {icon_path}")

    bots = manifest.get("bots", [])
    if len(bots) != 1:
        raise ValidationError("manifest must define exactly one bot")
    bot = bots[0]
    validate_guid(bot.get("botId", ""), "bots[0].botId")
    scopes = bot.get("scopes", [])
    if not scopes or any(scope not in {"personal", "team", "groupChat", "groupchat"} for scope in scopes):
        raise ValidationError("bots[0].scopes contains an invalid Teams scope")
    for command_list in bot.get("commandLists", []):
        if len(command_list.get("commands", [])) > 10:
            raise ValidationError("bot commandLists can contain at most 10 commands")

    for domain in manifest.get("validDomains", []):
        if "://" in domain:
            raise ValidationError(f"validDomains entry must be a hostname, not a URL: {domain}")


def validate_package_files(files: dict[str, bytes]) -> None:
    manifest_bytes = files.get("manifest.json")
    if manifest_bytes is None:
        raise ValidationError("package is missing required file: manifest.json")
    if manifest_bytes.startswith(b"\xef\xbb\xbf"):
        raise ValidationError("manifest.json must be UTF-8 without BOM")
    manifest_text = manifest_bytes.decode("utf-8")
    manifest = json.loads(manifest_text)
    validate_manifest(manifest, manifest_text)

    icon_paths = {
        icon_name: manifest["icons"][icon_name].replace("\\", "/")
        for icon_name in EXPECTED_ICON_SIZES
    }
    required = {"manifest.json", *icon_paths.values()}
    missing = sorted(required - set(files))
    if missing:
        raise ValidationError(f"package is missing required file(s): {', '.join(missing)}")

    allowed_roots = {"manifest.json", *(path.split("/")[0] for path in icon_paths.values())}
    extra_roots = sorted(name for name in files if name.split("/")[0] not in allowed_roots)
    if extra_roots:
        raise ValidationError(f"package contains unexpected root entries: {', '.join(extra_roots)}")

    for icon_name, expected_size in EXPECTED_ICON_SIZES.items():
        icon_path = icon_paths[icon_name]
        actual_size = read_png_size(files[icon_path])
        if actual_size != expected_size:
            raise ValidationError(
                f"{icon_path} must be {expected_size[0]}x{expected_size[1]}, got "
                f"{actual_size[0]}x{actual_size[1]}"
            )


def load_source(path: Path) -> dict[str, bytes]:
    manifest_bytes = (path / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8-sig"))
    files = {"manifest.json": manifest_bytes}
    for icon_name in EXPECTED_ICON_SIZES:
        icon_path = manifest["icons"][icon_name].replace("\\", "/")
        files[icon_path] = (path / icon_path).read_bytes()
    return files


def load_zip(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as package:
        return {
            name.replace("\\", "/"): package.read(name)
            for name in package.namelist()
            if not name.endswith("/")
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Microsoft Teams app package.")
    parser.add_argument("path", type=Path, help="Path to teams source directory or package zip.")
    args = parser.parse_args()

    try:
        files = load_zip(args.path) if args.path.suffix.lower() == ".zip" else load_source(args.path)
        validate_package_files(files)
    except (OSError, KeyError, json.JSONDecodeError, zipfile.BadZipFile, ValidationError) as exc:
        print(f"Teams package validation failed: {exc}", file=sys.stderr)
        return 1

    print(f"Teams package validation passed: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
