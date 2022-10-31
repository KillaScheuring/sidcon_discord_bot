from pprint import pprint


def get_final_scores(message_content):
    """
    Reads a message and returns the faction and final scores
    :param str message_content: The content of the message being read
    :return dict: The faction to score dictionary
    """

    if "-" not in message_content:
        return {}

    faction_rows = message_content.split("\n")
    return {faction: float(score) for faction, score in [row.split(" - ") for row in faction_rows if " - " in row]}


def calculate_confluence_score(final_scores):
    """
    Calculates the confluence score for a game
    :param dict final_scores: The scores for the game
    :return float: The confluence score of the game
    """

    scores = final_scores.values()
    return round(sum(scores) / (len(scores) - 1), 2)


if __name__ == '__main__':
    print(calculate_confluence_score({'Faderan': 38.0,
                                      "Im'dril Grand Fleet": 55.0,
                                      "K't": 53.0,
                                      'Unity': 46.0,
                                      'Yengii Jii': 61.5}))
