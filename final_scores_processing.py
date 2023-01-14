from pprint import pprint
from dotenv import load_dotenv
import pygsheets
import os
from datetime import date

load_dotenv()
GOOGLE_SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID')
client = pygsheets.authorize(service_account_env_var="SERVICE_ACCOUNT_KEY")


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

    message_content = message_content.replace("Kjas Independence", "Kjas Independents")

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
    factions = ["K't",
                "Caylion",
                "Kjas",
                "Faderan",
                "Eni Et",
                "Unity",
                "Im'dril",
                "Zeth",
                "Yengii",
                "K't Technophiles",
                "Caylion Collaborative",
                "Kjas Independents",
                "Society of Falling Light",
                "Eni Et Engineers",
                "Deep Unity",
                "Im'dril Grand Fleet",
                "Zeth Charity Syndicate",
                "Yengii Jii"]

    # Open the spreadsheet recording the final score data
    spreadsheet = client.open("Sidereal Confluence Final Scores")
    worksheet = spreadsheet.worksheet("title", "Final Scores")
    # Get the next unused row
    row_index = next_available_row(worksheet)

    # Add the date
    worksheet.cell(f"A{row_index}").value = game_date.strftime("%m/%d/%Y")
    # Add the confluence score, winner, and player count calculations
    worksheet.cell(f"B{row_index}").value = f"=ROUND(SUM(E{row_index}:V{row_index})/(D{row_index}-1), 1)"
    worksheet.cell(f"C{row_index}").value = f"=INDEX($E$1:$V$1,0," \
                                            f"MATCH(MAX($E{row_index}:$V{row_index}),$E{row_index}:$V{row_index},0))"
    worksheet.cell(f"D{row_index}").value = f"=COUNTA(E{row_index}:V{row_index})"

    # Loop through the factions and input the appropriate values from the final scores
    for index, faction in enumerate(factions):
        faction_cell = chr(index+ord("E")) + str(row_index)
        worksheet.cell(faction_cell).value = final_scores.get(faction, "")


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
