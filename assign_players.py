from pprint import pprint
from random import choice

sidereal_confluence_factions = [
    ["K't", "K't Technophiles"],
    ["Caylion", "Caylion Collaborative"],
    ["Kjas", "Kjas Independents"],
    ["Faderan", "Society of Falling Light"],
    ["Eni Et", "Eni Et Engineers"],
    ["Unity", "Deep Unity"],
    ["Im'dril", "Im'dril Grand Fleet"],
    ["Zeth", "Zeth Charity Syndicate"],
    ["Yengii", "Yengii Jii"]
]


def random_assignment(players):
    """
    Assigns Sidereal Confluence factions to players
    :param list players: The list of players to assign factions to
    :return dict: The assignments
    """
    assignments = {}
    for player in players:
        player_assignment = choice(sidereal_confluence_factions)
        sidereal_confluence_factions.remove(player_assignment)
        player_assignment = choice(player_assignment)
        assignments.setdefault(player, player_assignment)

    return assignments


if __name__ == '__main__':
    players_list = [
        "Bruce",
        "Tony",
        "Steve",
        "Clint",
        "Natasha"
    ]
    pprint(random_assignment(players_list))
