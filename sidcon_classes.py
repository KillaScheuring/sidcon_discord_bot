import json
import enum
from pprint import pprint

resource_emoji_dict = {
    "green": "<:green_cube:1122249567044374729>",
    "brown": "<:brown_cube:1122249460060274739>",
    "white": "<:white_cube:1122249631733141514>",
    "black": "<:black_cube:1122249185324961904>",
    "blue": "<:blue_cube:1122249285950521404>",
    "yellow": "<:yellow_cube:1122249354464481291>",
    "ultratech": "<:ultratech:1122249417681031321>",
}


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
        self.all = {
            "green": green,
            "brown": brown,
            "white": white,
            "black": black,
            "blue": blue,
            "yellow": yellow,
            "ultratech": ultratech,
            "large": large,
            "small": small,
        }

    def __getitem__(self, item):
        return self.all[item]


class StartCard:
    def __init__(self, resources: Resources | dict, colonies: int, research: int):
        self.resources = resources if type(resources) == Resources else Resources(**resources)
        self.colonies = colonies
        self.research_teams = research


class Faction:
    def __init__(self, version: Versions,
                 full: str, abbreviation: str, emoji: str,
                 exclusion: str, color: Color | dict, impact: int,
                 consumes: Resources | dict, produces: Resources | dict, start: StartCard | dict,
                 short: list[str] | str | None = None, order: int | None = None):
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
        self.start_with = start if type(start) == StartCard else StartCard(**start)
        self.order = order

        self.name = self.shortnames[0] if self.shortnames else self.fullname
        self.any_ref = [self.fullname, self.abbreviation, self.emoji, self.exclusion_role]
        if self.shortnames:
            self.any_ref.extend(self.shortnames)

    def __str__(self):
        return self.name


class Species:
    def __init__(self, base: Faction | dict, expansion: Faction | dict):
        self.base = base if type(base) == Faction else Faction(**base, version=Versions.Base)
        self.expansion = expansion if type(expansion) == Faction else Faction(**expansion, version=Versions.Expansion)

    def __str__(self):
        return self.base.name


class SpeciesList(list[Species]):
    def __init__(self):
        super().__init__()
        with open("species.json", "r") as species_file:
            for species in json.load(species_file):
                self.append(Species(**species))

    def find_faction(self,
                     any_ref: str | None = None,
                     fullname: str | None = None, shortname: str | None = None,
                     abbreviation: str | None = None, emoji: str | None = None,
                     exclusion_role: str | None = None):
        """

        :param str any_ref: Any alias
        :param str fullname: The fullname of the faction
        :param str shortname: The short name for the faction
        :param str abbreviation: The abbreviation of the faction
        :param str emoji: The emoji for the faction
        :param str exclusion_role: The role name that would exclude this faction during assignment
        :return: Faction
        """
        for race in self:
            if race.base.fullname == fullname or (race.base.shortnames and shortname in race.base.shortnames) or \
                    race.base.abbreviation == abbreviation or race.base.emoji == emoji or \
                    race.base.exclusion_role == exclusion_role or any_ref in race.base.any_ref:
                return race.base
            if race.expansion.fullname == fullname or \
                    (race.expansion.shortnames and shortname in race.expansion.shortnames) or \
                    race.expansion.abbreviation == abbreviation or race.expansion.emoji == emoji or \
                    race.expansion.exclusion_role == exclusion_role or any_ref in race.expansion.any_ref:
                return race.expansion
        return None

    def remove_by_faction(self, faction: Faction | None = None,
                          fullname: str | None = None, shortname: str | None = None,
                          abbreviation: str | None = None, emoji: str | None = None,
                          exclusion_role: str | None = None):
        """
        :param Faction | None faction: The faction to look up the race
        :param str | None fullname: The fullname of the faction
        :param str shortname: The short name for the faction
        :param str abbreviation: The abbreviation of the faction
        :param str emoji: The emoji for the faction
        :param str exclusion_role: The role name that would exclude this faction during assignment
        """
        if not faction:
            faction = self.find_faction(fullname, shortname, abbreviation, emoji, exclusion_role)
        for race in self:
            if race.base.abbreviation == faction.abbreviation or race.expansion.abbreviation == faction.abbreviation:
                self.remove(race)
                return

    def factions(self):
        """
        Returns the list of all factions base and expansion
        :return: list[Faction]
        """
        factions = []
        for species in self:
            factions.append(species.base)
            factions.append(species.expansion)
        factions.sort(key=lambda x: x.order)
        return factions


if __name__ == '__main__':
    # print(str(species_list[0].base))
    # print(str(species_list.find_faction(abbreviation="CC")))
    # species_list.remove_by_faction(faction=species_list[0].base)
    # species_list.remove_by_faction(fullname="Caylion Collaborative")
    # species_list.remove_by_faction(shortname="Kjas")
    # species_list.remove_by_faction(abbreviation="FL")
    # species_list.remove_by_faction(emoji="<:imdril:973968194974933053>")
    # species_list.remove_by_faction(exclusion_role="no-eni-et-engineers")
    species_list = SpeciesList()
    print(len(species_list))
    print([str(species) for species in species_list])
