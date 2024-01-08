import os
import discord
from discord.ext import commands
from discord import app_commands
from discord import Member, Interaction, Message
from dotenv import load_dotenv
from typing import Optional, List
from pprint import pprint
from datetime import timezone
from assign_players import random_assignment, structure_assignments, get_current_assignments
from final_scores_processing import get_final_scores, calculate_winner, \
    structure_response, report_to_sheet, reorder_final_scores
from manage_roles import find_role, emoji_to_exclusion
from exclusion_settings import ExclusionSettings
from assignment_interaction import AssignmentInteraction

# Get token from env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Define bot client
client = discord.Client(intents=intents)

# Define command tree
tree = app_commands.CommandTree(client)


@tree.command(name="poll", description="Creates a poll for a SidCon meet up")
@app_commands.describe(meet_up_message="The message purposing the meet up. (e.g. I have a need for cubes)",
                       meet_up_day="The proposed day for the meet up",
                       meet_up_time="The purposed time for the meet up")
@app_commands.rename(meet_up_message="message",
                     meet_up_day="day",
                     meet_up_time="time")
async def meet_up(interaction: Interaction,
                  meet_up_day: str,
                  meet_up_time: str,
                  meet_up_message: Optional[str] = None):
    """
    Generates a poll for planning a meet up
    :param interaction:
    :param meet_up_message:
    :param meet_up_day:
    :param meet_up_time:
    """
    poll_content = "@everyone\n" + \
                   (f"{meet_up_message}\n" if meet_up_message else "") + \
                   f"{meet_up_day} at {meet_up_time}\n" \
                   f":raised_hand:\tGoing\n" \
                   f":one:\tBringing a plus-one\n" \
                   f":fingers_crossed:\tMaybe\n"
    await interaction.response.send_message(poll_content)


@tree.command(name="factions", description="Manages which factions you would prefer not to get during assignment")
async def assign_exclusion(interaction: Interaction):
    """
    :param interaction:
    :return:
    """
    await interaction.response.send_message(view=ExclusionSettings(interaction.user), ephemeral=True)


@tree.command(name="assign", description="Manages which factions you would prefer not to get during assignment")
@app_commands.describe(player_assignment_1="Name/Mention[ - Faction]",
                       player_assignment_2="Name/Mention[ - Faction]",
                       player_assignment_3="Name/Mention[ - Faction]",
                       player_assignment_4="Name/Mention[ - Faction]",
                       player_assignment_5="Name/Mention[ - Faction]",
                       player_assignment_6="Name/Mention[ - Faction]",
                       player_assignment_7="Name/Mention[ - Faction]",
                       player_assignment_8="Name/Mention[ - Faction]",
                       player_assignment_9="Name/Mention[ - Faction]",
                       impact_limit="Impact Limit",
                       bifurcation_limit="Number of variants allowed"
                       )
@app_commands.rename(player_assignment_1="player1",
                     player_assignment_2="player2",
                     player_assignment_3="player3",
                     player_assignment_4="player4",
                     player_assignment_5="player5",
                     player_assignment_6="player6",
                     player_assignment_7="player7",
                     player_assignment_8="player8",
                     player_assignment_9="player9"
                     )
async def process_assignment(interaction: Interaction,
                             player_assignment_1: Optional[str] = None,
                             player_assignment_2: Optional[str] = None,
                             player_assignment_3: Optional[str] = None,
                             player_assignment_4: Optional[str] = None,
                             player_assignment_5: Optional[str] = None,
                             player_assignment_6: Optional[str] = None,
                             player_assignment_7: Optional[str] = None,
                             player_assignment_8: Optional[str] = None,
                             player_assignment_9: Optional[str] = None,
                             impact_limit: Optional[int] = 10,
                             bifurcation_limit: Optional[int] = 10
                             ):
    """
    Takes the provided combination of players and assigned factions and assigns the remaining
    :param Interaction interaction:
    :param Optional[str] player_assignment_1: A combination of player (name or mention) and faction (optional)
    :param Optional[str] player_assignment_2: A combination of player (name or mention) and faction (optional)
    :param Optional[str] player_assignment_3: A combination of player (name or mention) and faction (optional)
    :param Optional[str] player_assignment_4: A combination of player (name or mention) and faction (optional)
    :param Optional[str] player_assignment_5: A combination of player (name or mention) and faction (optional)
    :param Optional[str] player_assignment_6: A combination of player (name or mention) and faction (optional)
    :param Optional[str] player_assignment_7: A combination of player (name or mention) and faction (optional)
    :param Optional[str] player_assignment_8: A combination of player (name or mention) and faction (optional)
    :param Optional[str] player_assignment_9: A combination of player (name or mention) and faction (optional)
    :param Optional[int] impact_limit: The maximum allowed impact. Control for newer players.
    :param Optional[int] bifurcation_limit: The maximum number of allowed alternate factions. Control for newer players.
    """

    # Add all assignments to a list for easier processing
    assignments = []

    if player_assignment_1:
        assignments.append(player_assignment_1)
    if player_assignment_2:
        assignments.append(player_assignment_2)
    if player_assignment_3:
        assignments.append(player_assignment_3)
    if player_assignment_4:
        assignments.append(player_assignment_4)
    if player_assignment_5:
        assignments.append(player_assignment_5)
    if player_assignment_6:
        assignments.append(player_assignment_6)
    if player_assignment_7:
        assignments.append(player_assignment_7)
    if player_assignment_8:
        assignments.append(player_assignment_8)
    if player_assignment_9:
        assignments.append(player_assignment_9)

    current_assignments, player_exclusions = get_current_assignments(interaction, assignments)

    new_assignments = random_assignment(list(current_assignments.keys()),
                                        bifurcation_limit, impact_limit, current_assignments,
                                        player_exclusions)
    await interaction.response.send_message(structure_assignments(new_assignments),
                                            view=AssignmentInteraction(list(new_assignments.values())))


@client.event
async def on_ready():
    await tree.sync()
    print("Ready")


@client.event
async def on_message(message: Message):
    if message.channel.name != "final-scores" or message.author.bot:
        return

    final_scores = get_final_scores(message.content)
    if not final_scores:
        return

    sorted_message = await message.channel.send(content=reorder_final_scores(final_scores, message.author.id))
    await message.delete()

    winners, score = calculate_winner(final_scores)

    # Respond with the confluence score
    await sorted_message.reply(structure_response(final_scores, winners, score))

    # # Add final scores to spreadsheet
    # report_to_sheet(final_scores, winners, message.created_at.replace(tzinfo=timezone.utc).astimezone(tz=None))


# @bot.command(name="create-roles", help="Adds roles for bot operation")
# async def add_roles(ctx):
#     """
#     Adds the roles for exclusions during assignments
#     :param ctx:
#     :return:
#     """
#     if "Yengii" not in [role.name for role in ctx.message.author.roles]:
#         return
#
#     for faction in list_factions():
#         exclusion_role = faction.get("exclusion")
#         # role_color = Color(int(faction.get("color", {}).get("hex"), 16))
#         if exclusion_role not in [role.name for role in ctx.guild.roles]:
#             await ctx.guild.create_role(name=exclusion_role, colour=None)
#
#

if __name__ == '__main__':
    client.run(TOKEN)
