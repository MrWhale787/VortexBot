#pip install requests

import requests as req
import json

api_key = ""

def fetchMatch(RID):
    if len(api_key) != 40:
        return "invalid api key"
    try:
        int(RID)
        url = f"https://api.leaguecloud.org/sclbuild/getround?id={RID}&api_key={api_key}"
        try:
            response = req.get(url)
            output = response.json()
            if output["error"] != False:
                return output["message"]
            else:
                return [output["id"],output["data"]]
        except:
            return "invalid api key"
    except:
        return "invalid RID"
