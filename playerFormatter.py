#honestly this doesnt need to be a seperate library, im just trying to save main from looking like shit
import asyncio
import robloxAPI as rbx


async def formatTeam(team):
    fTeam = ""
    try:
        players = team.keys()
        players = list(players)
        usersInfo = await rbx.getUsersInfo(players)
        LB = []
        for i in (players):
            fplayer = team[i]
            for userData in usersInfo:
                if str(userData["id"]) == i:
                    userName = userData["name"]
                    break
            player = {"Name":userName,"Kills": fplayer["kills"],"Deaths": fplayer["deaths"],"Score": fplayer["score"]}
            LB.append(player.copy())
        LBSorted = sorted(LB, key=lambda k: k['Score'],reverse = True)
        for i in LBSorted:
            for k in i:
                 fTeam += str(k) + ': ' + str(i[k]) + ' '
            fTeam += '\n'
        return fTeam
    except:
        return "Empty"

async def formatMatches(matches):
    fmatches = ""
    for match in matches:
        fmatch = f'Map: {match[4]}, Mode: {match[5]}, Team: {match[3]},  Victor: {match[6]}\nKills: {match[0]}, Deaths: {match[1]}, KD: {round((match[0]/match[1]),2)}, Score: {match[2]}\n'
        fmatches = fmatches + f'\n{fmatch}'
    return fmatches
