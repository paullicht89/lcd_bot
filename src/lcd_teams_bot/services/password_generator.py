from __future__ import annotations

import secrets

SYMBOLS = "!#$%?@"

WORDS: tuple[str, ...] = (
    "anchor",
    "apple",
    "badge",
    "beacon",
    "bird",
    "bridge",
    "button",
    "cactus",
    "camera",
    "candle",
    "castle",
    "circle",
    "cloud",
    "coffee",
    "comet",
    "copper",
    "corner",
    "desk",
    "dragon",
    "eagle",
    "falcon",
    "field",
    "forest",
    "garden",
    "harbor",
    "island",
    "jacket",
    "ladder",
    "lantern",
    "maple",
    "market",
    "meadow",
    "meteor",
    "motion",
    "mountain",
    "ocean",
    "office",
    "orange",
    "pencil",
    "planet",
    "pocket",
    "rabbit",
    "river",
    "rocket",
    "shadow",
    "signal",
    "silver",
    "station",
    "stone",
    "summer",
    "table",
    "tablet",
    "tiger",
    "tunnel",
    "valley",
    "velvet",
    "window",
    "yellow",
    "zebra",
    "zipper",
)


def generate_password() -> str:
    word1 = _random_word()
    word2 = _random_word()
    number = secrets.randbelow(900) + 100
    symbol = secrets.choice(SYMBOLS)

    return f"{word1}-{word2}-{number}{symbol}"


def _random_word() -> str:
    return secrets.choice(WORDS).capitalize()
