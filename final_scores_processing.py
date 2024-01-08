from pprint import pprint
from dotenv import load_dotenv
import pygsheets
import os
from datetime import date
import re
from assign_players import list_factions, find_faction
from sidcon_classes import SpeciesList

load_dotenv()
GOOGLE_SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID')
client = pygsheets.authorize(service_account_env_var="SERVICE_ACCOUNT_KEY")
GOOGLE_SPREADSHEET = os.getenv("GOOGLE_SPREADSHEET")


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.get_col(1)))
    return str(len(str_list) + 1)


def get_final_scores(message_content):
    """
    Reads a message and returns the faction and final scores
    :param str message_content: The content of the message being read
    :return dict: The faction to score dictionary
    """

    if "-" not in message_content:
        return {}

    species_list = SpeciesList()

    message_content = re.sub("(\s+)(-)(\s+)", " - ", message_content)

    faction_rows = message_content.split("\n")
    return {
        species_list.find_faction(faction): float(score)
        for faction, score in
        [row.split(" - ") for row in faction_rows if " - " in row]
    }


def calculate_confluence_score(final_scores):
    """
    Calculates the confluence score for a game
    :param dict final_scores: The scores for the game
    :return float: The confluence score of the game
    """
    table_score = 0
    number_of_players = 0
    for faction, score in final_scores.items():
        # Check if faction is the Falling Light
        if faction.abbreviation != "FL":
            # If not, add the score to the tables score
            table_score += score
        number_of_players += 1
    return round(table_score / (number_of_players - 1), 2)


def calculate_winner(final_scores):
    """
    Calculates the confluence score for a game
    :param dict final_scores: The scores for the game
    :return float: The confluence score of the game
    """
    highest_score = max(list(final_scores.values()))
    winners = [faction for faction in final_scores if final_scores[faction] == highest_score]
    winners.sort(key=lambda x: x.order)
    return winners, highest_score


def report_to_sheet(final_scores, winners, game_date=None):
    """
    Takes the final scores and puts them into the Google sheet
    :param final_scores: The final scores from the Discord message
    :param winners: The winning factions
    :param game_date: The date of the message
    """
    if not game_date:
        game_date = date.today()

    sidereal_confluence_factions = SpeciesList().factions()
    final_scores = {faction.name: score for faction, score in final_scores.items()}

    # Open the spreadsheet recording the final score data
    spreadsheet = client.open(GOOGLE_SPREADSHEET)
    worksheet = spreadsheet.worksheet("title", "Final Scores")

    # Get the next unused row
    row_index = next_available_row(worksheet)

    # Loop through the factions and input the appropriate values from the final scores
    for index, faction in enumerate(sidereal_confluence_factions):
        faction_cell = chr(index + ord("E")) + str(row_index)
        if faction.name in final_scores:
            worksheet.cell(faction_cell).value = final_scores.get(faction.name)

    # Add the date
    worksheet.cell(f"A{row_index}").value = game_date.strftime("%m/%d/%Y")
    # Add the confluence score calculations
    worksheet.cell(f"B{row_index}").value = f"=ROUND((SUM(E{row_index}:V{row_index})-Q{row_index})/(D{row_index}-1), 1)"
    # Add the winner calculation
    worksheet.cell(f"C{row_index}").value = "/".join([winner.name for winner in winners])
    # Add the player count
    worksheet.cell(f"D{row_index}").value = f"=COUNTA(E{row_index}:V{row_index})"


def structure_response(final_scores, winners, score):
    """

    :param final_scores: The factions final scores
    :param winners: The winning factions
    :param score: The winning score
    :return:
    """
    confluence_score = calculate_confluence_score(final_scores)
    # Format winners
    winner_message = []
    for winner in winners:
        winner_message.append(f"{winner.emoji} {winner.name} with {score}")
    winner_message = "\n".join(winner_message)
    return f"Winner: \n" \
           f"{winner_message}\n" \
           f"\n" \
           f"Confluence Score: \n" \
           f"{confluence_score}"


if __name__ == '__main__':
    # print(calculate_confluence_score({'Faderan': 38.0,
    #                                   "Im'dril Grand Fleet": 55.0,
    #                                   "K't": 53.0,
    #                                   'Unity': 46.0,
    #                                   'Yengii Jii': 61.5}))
    print(report_to_sheet(get_final_scores("""Society of Falling Light - 33
Eni Et - 62
K't Technophiles - 52
Kjas Independence - 50
Im'dril - 42.5
Caylion - 44.5""")))
