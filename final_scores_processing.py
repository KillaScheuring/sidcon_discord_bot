from pprint import pprint
from dotenv import load_dotenv
import pygsheets
import os
from datetime import date
import re
from assign_players import list_factions

load_dotenv()
GOOGLE_SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID')
client = pygsheets.authorize(service_account_env_var="SERVICE_ACCOUNT_KEY")
GOOGLE_SPREADSHEET = os.getenv("GOOGLE_SPREADSHEET")


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.get_col(1)))
    return str(len(str_list)+1)


def get_final_scores(message_content):
    """
    Reads a message and returns the faction and final scores
    :param str message_content: The content of the message being read
    :return dict: The faction to score dictionary
    """

    if "-" not in message_content:
        return {}

    message_content = re.sub("(\s+)(-)(\s+)", " - ", message_content)

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


def report_to_sheet(final_scores, game_date=None):
    """
    Takes the final scores and puts them into the Google sheet
    :param final_scores: The final scores from the Discord message
    :param game_date: The date of the message
    """
    if not game_date:
        game_date = date.today()

    sidereal_confluence_factions = list_factions()

    # Open the spreadsheet recording the final score data
    spreadsheet = client.open(GOOGLE_SPREADSHEET)
    worksheet = spreadsheet.worksheet("title", "Final Scores")

    # Get the next unused row
    row_index = next_available_row(worksheet)

    pprint(final_scores)

    # Loop through the factions and input the appropriate values from the final scores
    for index, faction in enumerate(sidereal_confluence_factions):
        faction_cell = chr(index + ord("E")) + str(row_index)
        if faction.get("full") in final_scores or faction.get("emoji") in final_scores:
            worksheet.cell(faction_cell).value = \
                final_scores.get(faction.get("full"), final_scores.get(faction.get("emoji")))
        elif len(set(faction.get("short", [])) - set(final_scores.keys())) < len(faction.get("short", [])):
            for short_name in faction.get("short", []):
                if final_scores.get(short_name):
                    worksheet.cell(faction_cell).value = final_scores.get(short_name)

    # Add the date
    worksheet.cell(f"A{row_index}").value = game_date.strftime("%m/%d/%Y")
    # Add the confluence score calculations
    worksheet.cell(f"B{row_index}").value = f"=ROUND(SUM(E{row_index}:V{row_index})/(D{row_index}-1), 1)"
    # Add the winner calculation
    worksheet.cell(f"C{row_index}").value = f"=INDEX($E$1:$V$1,0," \
                                            f"MATCH(MAX($E{row_index}:$V{row_index}),$E{row_index}:$V{row_index},0))"
    # Add the player count
    worksheet.cell(f"D{row_index}").value = f"=COUNTA(E{row_index}:V{row_index})"


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
