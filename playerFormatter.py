#honestly this doesnt need to be a seperate library, im just trying to save main from looking like shit
import robloxAPI as rbx


def formatTeam(team):
    fTeam = ""
    players = team.keys()
    players = list(players)
    for i in range(len(players)):
        fplayer = team[str(players[i])]
        userInfo = rbx.getUserInfo(players[i])
        userName = userInfo["name"]
        player = {"Name":userName,"Kills": fplayer["kills"],"Deaths": fplayer["deaths"],"Score": fplayer["score"]}
        for k in player:
             fTeam += str(k) + ': ' + str(player[k]) + ' '
        fTeam += '\n'
    return fTeam
