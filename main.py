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

with open("config","r") as file:
    settings = json.load(file)
    uploadPerms = settings["uploadPerms"]





@client.event
async def on_ready():
    await Uploader.configure()
    print('Bot is ready')

#checks
def has_roles(roles):
    async def predicate(ctx):
        memberRoles = ctx.author.roles
        for role in memberRoles:
            if role.id in roles:
                return role.id in roles
    return commands.check(predicate)

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

uploadPerms = ['Recruitment']
@client.command()
@commands.has_permissions(administrator=True)
async def permSet(ctx,role : discord.Role ,permission):
    if permission.lower() == "upload":
        uploadPerms.append(role.id)
    with open("config","w") as file:
        settings["uploadPerms"] = uploadPerms
        json.dump(settings,file)

    await ctx.send("Permissions updated")


@client.command()
@has_roles(uploadPerms)
async def upload(ctx,roundID,mode="-v"):
    if mode != "-v":
        outcome = await Uploader.upload(roundID)
        await ctx.send(outcome)
        return
    else:
        outcome = await Uploader.upload(roundID)
        data = await LC.fetchMatch(roundID)
        await ctx.send(outcome)
        data = await LC.fetchMatch(roundID)
        if len(data) != 2:
            await ctx.send(data)
            return
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

@client.command(aliases=['whoIs','whois'])
async def queryPlayer(ctx,member : discord.Member):
    print(member.id)
    output = await Uploader.queryPlayerMatches(member.id)
    userName = await Uploader.queryPlayerName(member.id)
    if len(userName) == 0:
        await(ctx.send("Error player not found"))
        return
    userName = userName[0]
    stats = await Uploader.queryPlayerStats(member.id)
    stats = stats[0]
    totalKills = stats[0]
    totalDeaths = stats[1]
    KD = stats[2]



    matches = await Uploader.queryPlayerMatches(member.id)
    allMatches = await pF.formatMatches(matches)
    embed=discord.Embed(title=userName[0],description=f'**Statistics**\nKills: {totalKills} \nDeaths: {totalDeaths} \nKD: {round(KD,2)}')
    embed.add_field(name="Recent Matches", value=allMatches, inline=False)
    await ctx.send(embed=embed)


client.run(discAPI)
