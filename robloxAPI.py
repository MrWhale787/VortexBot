#roblox API handler, will probs rewrite in future, currentlys short term solution

import requests as req
import json


def getUserInfo(UID):
    url = f"https://users.roblox.com/v1/users/{UID}"
    response = req.get(url)
    output = response.json()
    if len(output) != 7:
        error = output[0]
        error = error[0]
        error = error["message"]
        return error
    else:
        return output
