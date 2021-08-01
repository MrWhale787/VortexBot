#honestly this doesnt need to be a seperate library, im just trying to save main from looking like shit
import asyncio
import robloxAPI as rbx


async def formatTeam(team):
    fTeam = ""
    players = team.keys()
    players = list(players)
    usersInfo = await rbx.getUsersInfo(players)
    for i in (players):
        fplayer = team[i]
        for userData in usersInfo:
            if str(userData["id"]) == i:
                userName = userData["name"]
                break
        player = {"Name":userName,"Kills": fplayer["kills"],"Deaths": fplayer["deaths"],"Score": fplayer["score"]}
        for k in player:
             fTeam += str(k) + ': ' + str(player[k]) + ' '
        fTeam += '\n'
    return fTeam
