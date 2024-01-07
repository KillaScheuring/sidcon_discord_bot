import os
import discord
from discord.ext import commands
from discord import app_commands
from discord import Member, Interaction
from dotenv import load_dotenv
from typing import Optional, List
from pprint import pprint
from datetime import timezone
from assign_players import random_assignment, structure_assignments, get_current_assignments, list_factions
from final_scores_processing import get_final_scores, structure_response, report_to_sheet
from manage_roles import find_role, emoji_to_exclusion
from exclusion_settings import ExclusionSettings

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


    :param Interaction interaction:
    :param Optional[str] player_assignment_1:
    :param Optional[str] player_assignment_2:
    :param Optional[str] player_assignment_3:
    :param Optional[str] player_assignment_4:
    :param Optional[str] player_assignment_5:
    :param Optional[str] player_assignment_6:
    :param Optional[str] player_assignment_7:
    :param Optional[str] player_assignment_8:
    :param Optional[str] player_assignment_9:
    :param Optional[int] impact_limit:
    :param Optional[int] bifurcation_limit:
    :return:
    """
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

    await interaction.response.send_message(structure_assignments(
        random_assignment(list(current_assignments.keys()),
                          bifurcation_limit, impact_limit, current_assignments,
                          player_exclusions)
    ), ephemeral=True
    )


@client.event
async def on_ready():
    await tree.sync()
    print("Ready")


# @bot.command(name="assign", help="Assigns random factions to players")
# async def random_assign_players(ctx, *players):
#     """
#     :param commands.context.Context ctx:
#     :param list players: The list of players to assign
#     """
#     if "\n" in ctx.message.content:
#         current_assignments, player_exclusions = get_current_assignments(ctx.message)
#         await ctx.message.reply(structure_assignments(
#             random_assignment(list(current_assignments.keys()), 10, current_assignments, player_exclusions)
#         ))
#     else:
#         await ctx.message.reply(structure_assignments(random_assignment(list(players), 10)))
#
#
# @bot.command(name="assign-control", help="Assigns factions to players and controls the number of alternates")
# async def random_assign_players(ctx, *players):
#     """
#     :param commands.context.Context ctx:
#     :param list players: The list of players to assign
#     """
#
#     if "\n" in ctx.message.content:
#         current_assignments, player_exclusions = get_current_assignments(ctx.message)
#         await ctx.message.reply(structure_assignments(
#             random_assignment(list(current_assignments.keys()), None, current_assignments, player_exclusions)
#         ))
#     else:
#         await ctx.message.reply(structure_assignments(random_assignment(list(players))))
#
#
# @bot.command(name="assign-selection", help="Assigns factions to players where some players have assignments")
# async def random_assign_selected(ctx):
#     """
#     :param ctx:
#     :return:
#     """
#     print(ctx.message.content)
#
#
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
# @bot.command(name="no", help="Add exclusion role to your user. For example, no-unity to not be assigned unity")
# async def assign_exclusion(ctx, *factions):
#     """
#
#     :param ctx:
#     :param factions:
#     :return:
#     """
#     role_names = emoji_to_exclusion(factions)
#     for role_name in role_names:
#         await ctx.message.author.add_roles(find_role(ctx, role_name))
#
#
# @bot.command(name="add", help="Remove exclusion role from your user. For example, no-unity to be assigned unity")
# async def assign_exclusion(ctx, *factions):
#     """
#
#     :param ctx:
#     :param factions:
#     :return:
#     """
#     role_names = emoji_to_exclusion(factions)
#     for role_name in role_names:
#         await ctx.message.author.remove_roles(find_role(ctx, role_name))


if __name__ == '__main__':
    client.run(TOKEN)
