#Main script for bot
import discord
import LeagueCloud as LC
import playerFormatter as pF
import Uploader
import robloxAPI as rbx
import json
from discord.ext import commands

client = commands.Bot(command_prefix = "vt!")
with open("api-keys.txt","r") as file:
     keys = json.load(file)
     discAPI = keys["discAPI"]
     LC.api_key = keys["LC-API"]


@client.event
async def on_ready():
    await Uploader.configure()
    print('Bot is ready')

@client.command(aliases=['match','m'])
async def view(ctx,roundID):
    data = await LC.fetchMatch(roundID)
    if len(data) != 2:
        await ctx.send(data)
    RID = data[0]
    matchData = data[1]
    playerStats = matchData["stats"]
    matchDetails = f'Map: {matchData["map"]}, Mode: {matchData["mode"]}, Victor: {matchData["victor"]}'
    phantoms = playerStats["Phantoms"]
    phantomsFormatted = await pF.formatTeam(phantoms)
    ghosts = playerStats["Ghosts"]
    ghostsFormatted = await pF.formatTeam(ghosts)
    embed=discord.Embed(title=RID)
    embed.add_field(name="Match Details", value=matchDetails , inline=False)
    embed.add_field(name="Phantoms", value=phantomsFormatted, inline=False)
    embed.add_field(name="Ghosts", value=ghostsFormatted, inline=False)
    await ctx.send(embed=embed)

role = "recruiter"
@client.command()
@commands.has_role(role)
async def upload(ctx,roundID):
    await Uploader.upload(roundID)
    await ctx.send("uploaded",roundID)

@client.command()
async def register(ctx,RobloxID):
    discordID = ctx.message.author.id
    robloxData = await rbx.getUserInfo(RobloxID)
    verificationString = await Uploader.addPlayer(robloxData,discordID)
    await ctx.send(f'Player Added, to verify please add the following string to your Roblox Profile Description and run vt!verify. verificationString: {verificationString}')

@client.command()
async def verify(ctx):


client.run(discAPI)
