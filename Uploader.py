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
    data = matchData[1]
    stats = data["stats"]
    playersList = []
    nameTeams = list(stats.keys())
    for i in range(len(stats)):
        team = nameTeams[i]
        teamData = stats[team]
        players = list(teamData.keys())
        for player in players:
            teamObjScore += (player["score"]-player["kills"]*100)
        for player in players:
            mmr = MMR.MMRcalc(playerData, teamObjScore, len(players)) #rawMMR
            playerData = teamData[str(player)]
            playerMatch = {"RID":int(matchData[0]),"RobloxID":int(players[i]),"Kills": int(playerData["kills"]),"Deaths": playerData["deaths"],"Score": playerData["score"],"Team":team, "MMR":mmr}
            playersList.append(playerMatch.copy())
    playerMatch = """
            INSERT INTO playerMatch(RID,RobloxID,Kills,Deaths,Score,Team,MMR) VALUES (:RID, :RobloxID, :Kills, :Deaths, :Score, :Team, :MMR)
            """
    match = f"""
            INSERT INTO matches(RID,Map,Mode,Victor) VALUES (:RID,:Map,:Mode,:Victor)
            """
    matchValues = {"RID":RID,"Map":data["map"],"Mode":data["mode"],"Victor":data["victor"]}

    for i in players:
        await addPlayer(i)

    try:
        await database.execute(query=match,values=matchValues)
        await database.execute_many(query=playerMatch, values=playersList)
        return f'{RID} uploaded'
    except:
        return f'{RID} already uploaded'
