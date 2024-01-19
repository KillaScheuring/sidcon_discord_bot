from pprint import pprint
from random import choice
from math import floor
import json
from discord.message import Message
from discord.utils import get
from discord.client import Client
from discord import Interaction, Member
import re
from sidcon_classes import SpeciesList


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
    return {}


def format_player_selection(faction):
    """

    :param faction:
    :return:
    """
    return faction.get("short", [faction.get("full")])[0], faction.get("emoji")


def get_current_assignments_2(message):
    """

    :param Message message:
    :return:
    """
    message_content = message.content

    exclusions = {}
    for user in message.mentions:
        message_content = message_content.replace(f"<@{user.id}>", user.name)
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


def get_current_assignments(interaction, current_assignments):
    """
    Collects each player's current assignment and
    retrieves each user's exclusions
    :param Interaction interaction:
    :param list[str] current_assignments:
    :return: dict, dict
    """
    exclusions = {}
    assignments = {}

    species_list = SpeciesList()

    # Retrieve user's exclusions
    for assignment in current_assignments:
        assignment = re.sub("(\s+)(-)(\s+)", " - ", assignment + " ")
        try:
            player, faction = assignment.split(" - ")
            faction = species_list.find_faction(any_ref=faction.strip())
        except ValueError:
            player, faction = assignment.strip(), None

        try:
            user_mention = re.search("<@[0-9]+>", player).group()
            user_id = re.search("[0-9]+", user_mention).group()
            player = interaction.guild.get_member(int(user_id))
        except AttributeError:
            player = player

        if type(player) == Member:
            for role in player.roles:
                if "no-" not in role.name:
                    continue
                exclusions.setdefault(f"<@{player.id}>", []).append(role.name)
            player = f"<@{player.id}>"
        assignments.setdefault(player, faction)

    return assignments, exclusions


def select_faction(exclusions, available_species, bifurcation_limit, impact_limit):
    """
    Selects an available faction for a player
    :param exclusions: The list of player exclusions
    :param SpeciesList available_species: The list of available species
    :param bifurcation_limit: The current bifurcation limit
    :param impact_limit: The current impact limit
    :return: selection
    """
    player_options = []
    for species in available_species:
        # Add the expansion faction if it isn't in the players excluded factions
        if species.expansion.exclusion_role not in exclusions:
            player_options.append(species.expansion)

        # Add the base faction if it isn't in the players excluded factions
        if species.base.exclusion_role not in exclusions:
            player_options.append(species.base)

    # If there are no qualifying factions for this player, they'll receive a random assignment
    if not player_options:
        return None

    player_selection = None
    for attempts in range(3):
        player_selection = choice(player_options)
        if (bifurcation_limit > 0 or player_selection.version == "base") \
                and impact_limit - player_selection.impact > 0:
            break
        player_options.remove(player_selection)

    return player_selection


def random_assignment(initial_player_assignment=None, player_exclusions=None,
                      bifurcation_limit=None, impact_limit=None):
    """
    Assigns Sidereal Confluence factions to players
    :param dict initial_player_assignment: The limit to how many alternate factions are in the game
    :param dict player_exclusions: The list of player faction exclusions
    :param int bifurcation_limit: The limit to how many alternate factions are in the game
    :param int impact_limit: The limit to how much total impact the factions have
    :return dict: The assignments
    """
    players = list(initial_player_assignment.keys())
    # If no bifurcation limit, set to a third of the players
    if bifurcation_limit is None:
        bifurcation_limit = floor(len(players) / 3)

    # If no impact limit, set to 3
    if impact_limit is None:
        impact_limit = 3

    # If no current players set to empty dictionary
    if initial_player_assignment is None:
        current_player_assignment = {}

    # Remove species already assigned
    available_species = SpeciesList()
    for faction in initial_player_assignment.values():
        if not faction:
            continue
        impact_limit -= faction.impact
        bifurcation_limit -= 0 if faction.version == "base" else 1
        available_species.remove_by_faction(faction)

    current_player_assignment = initial_player_assignment.copy()

    # Loop through players with exclusions
    for player in player_exclusions:
        # Skip if player already has an assignment
        if current_player_assignment[player]:
            continue

        player_selection = select_faction(player_exclusions[player], available_species, bifurcation_limit, impact_limit)

        if player_selection:
            bifurcation_limit -= 0 if player_selection.version == "base" else 1
            impact_limit -= player_selection.impact
            available_species.remove_by_faction(player_selection)
            current_player_assignment[player] = player_selection

    # Loop through players to assign faction
    for player in players:
        # Skip if player already has an assignment
        if current_player_assignment[player]:
            continue

        player_selection = select_faction([], available_species, bifurcation_limit, impact_limit)

        if player_selection:
            bifurcation_limit -= 0 if player_selection.version == "base" else 1
            impact_limit -= player_selection.impact
            available_species.remove_by_faction(player_selection)
            current_player_assignment[player] = player_selection

    return current_player_assignment


def structure_assignments(assignments):
    """
    :param assignments: The dictionary of player assignments
    :return:
    """
    assignments = {player: (faction.name, faction.emoji) for player, faction in assignments.items()}
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
