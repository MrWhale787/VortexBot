#Basic Data Uploader (links with sqlite3, will rewrite once i have made full database)
import LeagueCloud as LC
from databases import Database
database = Database('sqlite:///VortexData.db')

async def configure():
    await database.connect()
    try:
        query = """
                CREATE TABLE RoundData(
                ID INTEGER PRIMARY KEY,
                RID INTEGER NOT NULL,
                RobloxID INTEGER NOT NULL,
                Kills INTEGER NOT NULL,
                Deaths INTEGER NOT NULL,
                Score INTEGER NOT NULL,
                Team TEXT NOT NULL
                )
                """
        await database.execute(query=query)
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
