#honestly this doesnt need to be a seperate library, im just trying to save main from looking like shit

def formatTeam(team):
    fTeam = ""
    players = team.keys()
    players = list(players)
    for i in range(len(players)):
        fplayer = team[str(players[i])]
        player = {"Name":players[i],"Kills": fplayer["kills"],"Deaths": fplayer["deaths"],"Score": fplayer["score"]}
        for k in player:
             fTeam += str(k) + ': ' + str(player[k]) + ' '
        fTeam += '\n'
    return fTeam
