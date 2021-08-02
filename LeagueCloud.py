
import asyncio
import aiohttp

api_key = ""

async def fetchMatch(RID):
    if len(api_key) != 40:
        return "invalid api key"
    try:
        int(RID)
        url = f"https://api.leaguecloud.org/sclbuild/getround?id={RID}&api_key={api_key}"
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(url)
                output = await response.json()
            if output["error"] != False:
                return output["message"]
            else:
                return [output["id"],output["data"]]
        except:
            return "invalid api key"
    except:
        return "invalid RID"
