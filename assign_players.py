from pprint import pprint
from random import choice
from math import floor
import json


def open_species():
    with open("species.json", "r") as species_file:
        return json.load(species_file)


def get_current_assignments(message_content):
    """

    :param str message_content:
    :return:
    """
    assignments = {}
    for assignment in message_content.split("\n")[1:]:
        if len(assignment.split(" - ")) < 2:
            assignments.setdefault(assignment.replace(" -", ""), None)
        else:
            assignments.setdefault(assignment.split(" - ")[0], assignment.split(" - ")[1])
    return assignments


def random_assignment(players, alternate_limit=None, current_player_assignment=None):
    """
    Assigns Sidereal Confluence factions to players
    :param list players: The list of players to assign factions to
    :param int alternate_limit: The limit to how many alternate factions are in the game
    :param dict current_player_assignment: The limit to how many alternate factions are in the game
    :return dict: The assignments
    """
    if alternate_limit is None:
        alternate_limit = floor(len(players) / 3)
    if current_player_assignment is None:
        current_player_assignment = {}
    sidereal_confluence_factions = []
    for faction in open_species():
        if faction.get("base", {}).get("emoji", "") in current_player_assignment.values():
            continue

        if faction.get("expansion", {}).get("emoji", "") in current_player_assignment.values():
            alternate_limit -= 1
            continue

        sidereal_confluence_factions.append(faction)

    assignments = {player: ("", emoji) for player, emoji in current_player_assignment.items() if emoji}

    for player in players:
        player_species = choice(sidereal_confluence_factions)
        sidereal_confluence_factions.remove(player_species)
        if alternate_limit == 0:
            player_faction_version = "base"
        else:
            player_faction_version = choice(["base", "expansion"])
        alternate_limit -= 1 if player_faction_version == "expansion" else 0
        player_assignment = player_species[player_faction_version] \
            .get("short", player_species[player_faction_version].get("full"))
        player_emoji = player_species[player_faction_version].get("emoji")
        # print(player, player_assignment)
        assignments.setdefault(player, (player_assignment, player_emoji))
    # pprint(assignments)
    return assignments


def structure_assignments(assignments):
    """
    :param assignments:
    :return:
    """
    return "Assignments!\n" + \
           "\n".join([
               f"{player} - {emoji} {faction}" for player, (faction, emoji)
               in assignments.items()
           ])


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
    # pprint(random_assignment_controlled(list(players_list)))
    print("Assignments!\n" +
          "\n".join([
              f"{player} - {faction} :{emoji}:" for player, (faction, emoji)
              in random_assignment(list(players_list)).items()
          ]))
