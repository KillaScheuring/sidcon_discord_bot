import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from pprint import pprint
from assign_players import random_assignment

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} is connected')


@client.event
async def on_message(message):
    """
    Responds to specific messages
    :param discord.message.Message message: The message from the server
    """
    # print(type(message))
    print(message.author)
    print(client.user)
    if message.author == client.user:
        return
    print(message.channel_mentions)
    print("message.content", type(message.content), message.content)
    if message.content == "assign!":
        print("assign!")

    await message.channel.send("test back")


@bot.command(name="assign", help="Assigns players to factions")
async def assign_players(ctx, *players):
    """
    :param commands.context.Context ctx:
    :param list players: The list of players to assign
    """

    print(ctx.command)
    print(players)
    await ctx.message.reply("Assignments!\n" +
                            "\n".join([
                                f"{player} - {faction}" for player, faction in random_assignment(list(players)).items()
                            ]))


if __name__ == '__main__':
    # client.run(TOKEN)
    bot.run(TOKEN)
