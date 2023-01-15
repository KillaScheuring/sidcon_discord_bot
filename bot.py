import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pprint import pprint
from datetime import date, timezone
from assign_players import random_assignment, structure_assignments, get_current_assignments
from final_scores_processing import get_final_scores, calculate_confluence_score, report_to_sheet

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_message(message):
    """
    Responds to specific messages
    :param discord.message.Message message: The message from the server
    """
    if message.channel.name != "final-scores":
        await bot.process_commands(message)
        return

    final_scores = get_final_scores(message.content)
    if not final_scores:
        return

    # print(message.created_at)
    # print(message.created_at.replace(tzinfo=timezone.utc).astimezone(tz=None))

    # Respond with the confluence score
    confluence_score = calculate_confluence_score(final_scores)
    await message.reply(f"Confluence Score: {confluence_score}")

    # Add final scores to spreadsheet
    report_to_sheet(final_scores, message.created_at.replace(tzinfo=timezone.utc).astimezone(tz=None))


@bot.command(name="assign", help="Assigns random factions to players")
async def random_assign_players(ctx, *players):
    """
    :param commands.context.Context ctx:
    :param list players: The list of players to assign
    """
    if "\n" in ctx.message.content:
        current_assignments = get_current_assignments(ctx.message.content)
        await ctx.message.reply(structure_assignments(
            random_assignment(list(current_assignments.keys()), 10, current_assignments)
        ))
    else:
        await ctx.message.reply(structure_assignments(random_assignment(list(players), 10)))


@bot.command(name="assign-control", help="Assigns factions to players and controls the number of alternates")
async def random_assign_players(ctx, *players):
    """
    :param commands.context.Context ctx:
    :param list players: The list of players to assign
    """

    if "\n" in ctx.message.content:
        current_assignments = get_current_assignments(ctx.message.content)
        await ctx.message.reply(structure_assignments(
            random_assignment(list(current_assignments.keys()), None, current_assignments)
        ))
    else:
        await ctx.message.reply(structure_assignments(random_assignment(list(players))))


@bot.command(name="assign-selection", help="Assigns factions to players where some players have assignments")
async def random_assign_selected(ctx):
    """
    :param ctx:
    :return:
    """
    print(ctx.message.content)


if __name__ == '__main__':
    bot.run(TOKEN)
