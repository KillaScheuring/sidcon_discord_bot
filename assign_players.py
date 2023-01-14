from pprint import pprint
from random import choice
from math import floor

sidereal_confluence_factions = [
  {
    "base": {
      "full": "KT’ZR’KT’RTL",
      "short": "Kit"
    },
    "expansion": {
      "full": "KT’ZR’KT’RTL Technophiles",
      "short": "Kit Technophiles"
    }
  },
  {
    "base": {
      "full": "Caylion"
    },
    "expansion": {
      "full": "Caylion Collaborative"
    }
  },
  {
    "base": {
      "full": "Kjasjavikalimm",
      "short": "Kjas"
    },
    "expansion": {
      "full": "Kjasjavikalimm Independent Nations",
      "short": "Kjas Independent Nations"
    }
  },
  {
    "base": {
      "full": "Faderan"
    },
    "expansion": {
      "full": "Society of Falling Light"
    }
  },
  {
    "base": {
      "full": "Im’dril"
    },
    "expansion": {
      "full": "Grand Fleet"
    }
  },
  {
    "base": {
      "full": "Eni Et"
    },
    "expansion": {
      "full": "Eni Et Engineers"
    }
  },
  {
    "base": {
      "full": "Unity"
    },
    "expansion": {
      "full": "Deep Unity"
    }
  },
  {
    "base": {
      "full": "Yengii"
    },
    "expansion": {
      "full": " Yengii Ji"
    }
  },
  {
    "base": {
      "full": "Zeth"
    },
    "expansion": {
      "full": "Charity Syndicate"
    }
  }
]


def random_assignment(players):
    """
    Assigns Sidereal Confluence factions to players
    :param list players: The list of players to assign factions to
    :return dict: The assignments
    """
    assignments = {}
    for player in players:
        player_species = choice(sidereal_confluence_factions)
        sidereal_confluence_factions.remove(player_species)
        player_faction_version = choice(["base", "expansion"])
        player_assignment = player_species[player_faction_version] \
            .get("short", player_species[player_faction_version].get("full"))
        assignments.setdefault(player, player_assignment)

    return assignments


def random_assignment_controlled(players):
    """
    Assigns Sidereal Confluence factions to players
    :param list players: The list of players to assign factions to
    :return dict: The assignments
    """
    alternate_limit = floor(len(players)/3)
    print(alternate_limit)
    assignments = {}
    for player in players:
        player_species = choice(sidereal_confluence_factions)
        sidereal_confluence_factions.remove(player_species)
        if alternate_limit == 0:
            player_faction_version = "base"
        else:
            player_faction_version = choice(["base", "expansion"])
        alternate_limit -= 1 if player_faction_version == "expansion" else 0
        player_assignment = player_species[player_faction_version]\
            .get("short", player_species[player_faction_version].get("full"))
        # print(player, player_assignment)
        assignments.setdefault(player, player_assignment)
    # pprint(assignments)
    return assignments


if __name__ == '__main__':
    # players_list = [
    #     "Bruce",
    #     "Tony",
    #     "Steve",
    #     "Clint",
    #     # "Natasha",
    #     # "Pepper"
    # ]
    players_list = [
        "test1",
        "test2",
        "test3",
        "test4",
        # "Natasha",
        # "Pepper"
    ]
    # pprint(random_assignment(players_list))
    # pprint(random_assignment_controlled(players_list))
    print("Assignments!\n" +
                            "\n".join([
                                f"{player} - {faction}" for player, faction
                                in random_assignment_controlled(list(players_list)).items()
                            ]))
