from pprint import pprint
from random import choice
from math import floor
import json
from discord.message import Message


def open_species():
    """

    :return: list
    """
    with open("species.json", "r") as species_file:
        return json.load(species_file)


def list_factions():
    """

    :return: list
    """
    with open("species.json", "r") as species_file:
        species_list = json.load(species_file)
        faction_list = []
        for species in species_list:
            faction_list.append(species.get("base"))
        for species in species_list:
            faction_list.append(species.get("expansion"))
        return faction_list


def find_faction(faction_label):
    """

    :param faction_label:
    :return: dict
    """
    factions = list_factions()
    for faction in factions:
        if faction.get("emoji") == faction_label:
            return faction
        if faction.get("full") == faction_label:
            return faction
        if faction_label in faction.get("short", []):
            return faction


def get_current_assignments(message):
    """

    :param Message message:
    :return:
    """
    message_content = message.content

    exclusions = {}
    for user in message.mentions:
        message_content.replace(f"<@{user.id}>", user.name)
        for role in user.roles:
            if "no-" not in role.name:
                continue
            exclusions.setdefault(user.name, []).append(role.name)

    assignments = {}
    for assignment in message_content.split("\n")[1:]:
        # Get player and current assignment
        assignment = assignment.strip() + " "
        player, faction = assignment.split(" - ")
        assignments.setdefault(player.strip(), faction.strip())

    return assignments, exclusions


def random_assignment(players, alternate_limit=None, current_player_assignment=None):
    """
    Assigns Sidereal Confluence factions to players
    :param list players: The list of players to assign factions to
    :param int alternate_limit: The limit to how many alternate factions are in the game
    :param dict current_player_assignment: The limit to how many alternate factions are in the game
    :return dict: The assignments
    """
    # If no alternate limit, set to a third of the players
    if alternate_limit is None:
        alternate_limit = floor(len(players) / 3)

    # If no current players set to empty dictionary
    if current_player_assignment is None:
        current_player_assignment = {}

    # Remove species already assigned
    sidereal_confluence_factions = []
    for faction in open_species():
        # Check if base version of faction is already assigned
        if faction.get("base", {}).get("emoji", "") in current_player_assignment.values():
            continue

        # Check if expansion version of faction is already assigned
        if faction.get("expansion", {}).get("emoji", "") in current_player_assignment.values():
            # Record to alternate limit
            alternate_limit -= 1
            continue
        # Add species to assignable factions
        sidereal_confluence_factions.append(faction)

    # Create assignments dictionary and add current assignments
    assignments = {player: ("", emoji) for player, emoji in current_player_assignment.items() if emoji}

    # Loop through players to assign faction
    for player in players:
        # Skip if player already has an assignment
        if player in assignments:
            continue

        # Pick a species for the player
        player_species = choice(sidereal_confluence_factions)
        # Remove the pick from available species to keep other players from getting it
        sidereal_confluence_factions.remove(player_species)

        # Pick the version
        if alternate_limit <= 0:
            # Pick base if expansion allowance out
            player_faction_version = "base"
        else:
            # Randomly pick base or expansion
            player_faction_version = choice(["base", "expansion"])
        # Record to alternate limit
        alternate_limit -= 1 if player_faction_version == "expansion" else 0

        # Add short name and emoji to assignments dictionary
        player_assignment = player_species[player_faction_version] \
            .get("short", [player_species[player_faction_version].get("full")])[0]
        player_emoji = player_species[player_faction_version].get("emoji")
        assignments.setdefault(player, (player_assignment, player_emoji))
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
