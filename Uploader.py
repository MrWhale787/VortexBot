#Basic Data Uploader (links with sqlite3, will rewrite once i have made full database)
import LeagueCloud as LC
import robloxAPI as rbx
import MMR
import random
import string
from databases import Database
database = Database('sqlite:///VortexData.db')

#database configurator - only runs on initial setup
async def configure():
    await database.connect()
    query = "PRAGMA foreign_keys = ON"
    await database.execute(query=query)
    try:
        createPlayers = """
                CREATE TABLE players(
                RobloxID PRIMARY KEY,
                DiscordID INTEGER,
                DisplayName TEXT
                )
                """
        createMatches = """
                CREATE TABLE matches(
                RID PRIMARY KEY,
                Map TEXT,
                Mode TEXT,
                Victor TEXT
                )
                """
        createPlayerMatch = """
                CREATE TABLE playerMatch(
                ID INTEGER PRIMARY KEY,
                RID INTEGER NOT NULL,
                RobloxID INTEGER NOT NULL,
                Kills INTEGER NOT NULL,
                Deaths INTEGER NOT NULL,
                Score INTEGER NOT NULL,
                Team TEXT NOT NULL,
                MMR FLOAT NOT NULL,
                FOREIGN KEY (RID) REFERENCES matches (RID),
                FOREIGN KEY (RobloxID) REFERENCES players (RobloxID)
                )
                """
        await database.execute(query=createPlayers)
        await database.execute(query=createMatches)
        await database.execute(query=createPlayerMatch)
    except:
        print("database already exists continuing")

#add player to database
async def addPlayer(robloxID):
    robloxData = await rbx.getUserInfo(robloxID)
    DiscordID = await LC.fetchUser(robloxID)
    DiscordID = DiscordID["discord_id"]
    Player = {"RobloxID":robloxID,"DiscordID":DiscordID,"DisplayName":robloxData["name"]}
    try:
        query = """
                INSERT INTO Players(RobloxID,DiscordID,DisplayName) VALUES (:RobloxID, :DiscordID, :DisplayName)
                """
        await database.execute(query=query, values=Player)
        return "You are now registered"
    except:
        return "You are already registered"

#upload rounds to database
async def upload(RID):
    matchData = await LC.fetchMatch(RID)
    if len(matchData) != 2:
        return matchData
    data = matchData[1]
    stats = data["stats"]
    playersList = []
    teamScores = []
    nameTeams = list(stats.keys())
	
	#calculate teamRatios
    for i in range(len(stats)):
        teamObjScore = 0
        team = nameTeams[i]
        teamData = stats[team]
        for player in teamData:
            player = teamData[player]
            teamObjScore += (player["score"] - player["kills"]*100)
        teamScores.append(teamObjScore)
	

    if data["victor"] == "Phantoms":
        teamRatio = teamScores[0]/teamScores[1]
    elif data["victor"] == "Ghosts":
        teamRatio = teamScores[1]/teamScores[0]
    else:
        teamRatio = 1
		



	#arrange in record form and execute sql query
    for i in range(len(stats)):
        teamObjScore = 0
        team = nameTeams[i]
        teamData = stats[team]
        players = list(teamData.keys())
        for player in teamData:
            player = teamData[player]
            teamObjScore += (player["score"]-player["kills"]*100)
        for player in players:
            await addPlayer(player)
            playerData = teamData[str(player)]
            if playerData["score"] == 0:
                continue
            mmr = await MMR.MMRcalc(playerData, teamObjScore, len(players),team,data["victor"],teamRatio) #rawMMR
            playerMatch = {"RID":int(matchData[0]),"RobloxID":int(player),"Kills": int(playerData["kills"]),"Deaths": playerData["deaths"],"Score": playerData["score"],"Team":team, "MMR":mmr}
            playersList.append(playerMatch.copy())
    playerMatch = """
            INSERT INTO playerMatch(RID,RobloxID,Kills,Deaths,Score,Team,MMR) VALUES (:RID, :RobloxID, :Kills, :Deaths, :Score, :Team, :MMR)
            """
    match = f"""
            INSERT INTO matches(RID,Map,Mode,Victor) VALUES (:RID,:Map,:Mode,:Victor)
            """
    matchValues = {"RID":RID,"Map":data["map"],"Mode":data["mode"],"Victor":data["victor"]}

    try:
        await database.execute(query=match,values=matchValues)
        await database.execute_many(query=playerMatch, values=playersList)
        return f'{RID} uploaded'
    except:
        return f'{RID} already uploaded'

async def queryPlayerMatches(discordID):
    query = f"SELECT Kills, Deaths, Score, Team, matches.Map As Map, matches.Mode as Mode FROM playerMatch INNER JOIN players ON players.RobloxID = playerMatch.RobloxID INNER JOIN matches ON matches.RID = playerMatch.RID WHERE players.DiscordID = {discordID}"
    output = await database.fetch_all(query=query)
    return output

async def queryPlayerName(discordID):
    query = f"SELECT displayName FROM players WHERE players.DiscordID = {discordID}"
    output = await database.fetch_all(query=query)
    return output

async def queryPlayerStats(discordID):
    query = f'SELECT  SUM(Kills) AS Total_Kills, SUM(Deaths) AS Total_Deaths, AVG(Kills) / AVG(Deaths) AS KD FROM playerMatch INNER JOIN players ON players.RobloxID = playerMatch.RobloxID WHERE players.DiscordID = {discordID}'
    output = await database.fetch_all(query=query)
    return output


async def queryMatch(RID):
    query = f'SELECT RID, players.DisplayName, Kills, Deaths, Score, Team FROM playerMatch INNER JOIN players ON players.RobloxID = playerMatch.RobloxID WHERE RID = {RID}'
    output = await database.execute(query=query)
    return output
