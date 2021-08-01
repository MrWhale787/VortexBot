#Main script for bot
import discord
import LeagueCloud as LC
import playerFormatter as pF
from discord.ext import commands

client = commands.Bot(command_prefix = "vt!")
LC.api_key = '2ux1zyiE5vxjkEHjcn4ZeFYlfTEufGnRG1nQTbbg'

@client.event
async def on_ready():
    print('Bot is ready')

@client.command(aliases=['match','m'])
async def view(ctx,roundID):
    data = LC.fetchMatch(roundID)
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




client.run('ODcxMjc3NjExMjYxNzg4MTcw.YQY-gg.k_PNrzt5NvIkraKNU5pfuHavMj4')
