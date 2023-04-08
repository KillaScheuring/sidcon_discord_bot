import os
import discord
from discord.ext import commands
from discord import app_commands
from discord import Member, Interaction
from dotenv import load_dotenv
from pprint import pprint
from datetime import timezone
from assign_players import random_assignment, structure_assignments, get_current_assignments, list_factions
from final_scores_processing import get_final_scores, structure_response, report_to_sheet
from manage_roles import find_role, emoji_to_exclusion
from exclusion_questionnaire import ExclusionQuestionnaire

# Get token from env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define bot intents
intents = discord.Intents.default()
intents.message_content = True

# Define bot client
client = discord.Client(intents=intents)

# Define command tree
tree = app_commands.CommandTree(client)


@tree.command(name="no", description="Adds a role to keep user from being assigned that faction", guild=discord.Object(id=934254109605908600))
# @app_commands.describe(faction="The faction to exclude")
# async def assign_exclusion(interaction: Interaction, faction: str):
async def assign_exclusion(interaction: Interaction):
    """
    :param interaction:
    :return:
    """
    await interaction.response.send_message(view=ExclusionQuestionnaire(), ephemeral=True)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=934254109605908600))
    print("Ready")

# @bot.event
# async def on_message(message):
#     """
#     Responds to specific messages
#     :param discord.message.Message message: The message from the server
#     """
#     if message.channel.name != "final-scores":
#         await bot.process_commands(message)
#         return
#
#     final_scores = get_final_scores(message.content)
#     if not final_scores:
#         return
#
#     # Respond with the confluence score
#     await message.reply(structure_response(final_scores))
#
#     # Add final scores to spreadsheet
#     report_to_sheet(final_scores, message.created_at.replace(tzinfo=timezone.utc).astimezone(tz=None))
#
#
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
