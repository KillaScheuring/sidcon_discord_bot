import json
import enum


class Versions(enum.Enum):
    Base = "base"
    Expansion = "expansion"


class Color:
    def __init__(self, hex_code: str, rgb: list[int]):
        self.hex_code = hex_code
        self.rgb = rgb


class Resources:
    def __init__(self, green: int = 0, brown: int = 0, white: int = 0,
                 black: int = 0, blue: int = 0, yellow: int = 0,
                 ultratech: int = 0, large: int = 0, small: int = 0):
        self.green = green
        self.brown = brown
        self.white = white
        self.black = black
        self.blue = blue
        self.yellow = yellow
        self.ultratech = ultratech
        self.large = large
        self.small = small


class Faction:
    def __init__(self, version: Versions,
                 full: str, short: list[str] | str | None, abbreviation: str, emoji: str,
                 exclusion: str, color: Color | dict, impact: int,
                 consumes: Resources | dict, produces: Resources | dict, start: Resources | dict):
        self.version = version
        self.fullname = full
        self.shortnames = [short] if type(short) == str else short
        self.abbreviation = abbreviation
        self.emoji = emoji
        self.exclusion_role = exclusion
        self.color = color if type(color) == Color else Color(hex_code=color.get("hex"), rgb=color.get("rbg"))
        self.impact = impact
        self.consumes = consumes if type(consumes) == Resources else Resources(**consumes)
        self.produces = produces if type(produces) == Resources else Resources(**produces)
        self.start_with = start if type(start) == Resources else Resources(**start)

        self.name = self.shortnames[0] if self.shortnames else self.fullname


class Species:
    def __init__(self, base: Faction, expansion: Faction):
        self.base = base
        self.expansion = expansion


class
