import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pprint import pprint
from assign_players import random_assignment
from final_scores_processing import get_final_scores, calculate_confluence_score

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

    confluence_score = calculate_confluence_score(final_scores)
    await message.reply(f"Confluence Score: {confluence_score}")


@bot.command(name="assign", help="Assigns players to factions")
async def assign_players(ctx, *players):
    """
    :param commands.context.Context ctx:
    :param list players: The list of players to assign
    """

    await ctx.message.reply("Assignments!\n" +
                            "\n".join([
                                f"{player} - {faction}" for player, faction in random_assignment(list(players)).items()
                            ]))


if __name__ == '__main__':
    bot.run(TOKEN)
