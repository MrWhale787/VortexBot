#Main script for bot
import discord
from discord.ext import commands

client = commands.Bot(command_prefix = "vt!")

@client.event
async def on_ready():
    print('Bot is ready')

client.run('api key here')
