#Basic Data Uploader (links with sqlite3, will rewrite once i have made full database)
import LeagueCloud as LC
import random
import string
from databases import Database
database = Database('sqlite:///VortexData.db')

async def configure():
    await database.connect()
    query = "PRAGMA foreign_keys = ON"
    await database.execute(query=query)
    try:
        createPlayers = """
                CREATE TABLE players(
                RobloxID PRIMARY KEY,
                DiscordID INTEGER,
                DisplayName TEXT,
                VerificationString TEXT,
                Verified INTEGER
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
                FOREIGN KEY (RID) REFERENCES matches (RID),
                FOREIGN KEY (RobloxID) REFERENCES players (RobloxID)
                )
                """
        await database.execute(query=createPlayers)
        await database.execute(query=createMatches)
        await database.execute(query=createPlayerMatch)
    except:
        print("database already exists continuing")

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
            playerData = teamData[str(player)]
            playerMatch = {"RID":int(matchData[0]),"RobloxID":int(players[i]),"Kills": int(playerData["kills"]),"Deaths": playerData["deaths"],"Score": playerData["score"],"Team":team}
            playersList.append(playerMatch.copy())
    print(playersList)
    query = """
            INSERT INTO RoundData(RID,RobloxID,Kills,Deaths,Score,Team) VALUES (:RID, :RobloxID, :Kills, :Deaths, :Score, :Team)
            """
    await database.execute_many(query=query, values=playersList)

async def addPlayer(robloxData, DiscordID):
    verificationString = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    Player = {"RobloxID":robloxData["id"],"DiscordID":DiscordID,"DisplayName":robloxData["name"],"VerificationString":verificationString,"Verified":0}
    query = """
            INSERT INTO Players(RobloxID,DiscordID,DisplayName,VerificationString,Verified) VALUES (:RobloxID, :DiscordID, :DisplayName, :VerificationString, :Verified)
            """
    await database.execute(query=query, values=Player)
    return verificationString

async def queryPlayer(DiscordID):
    query = f'SELECT FROM players(RobloxID,DiscordID,VerificationString) WHERE DiscordID = {DiscordID}'
    output = await database.execute(query=query)
    return output
