#roblox API handler, will probs rewrite in future, currentlys short term solution
import asyncio
import aiohttp
import json


async def getUserInfo(UID):
    async with aiohttp.ClientSession() as session:
        url = f"https://users.roblox.com/v1/users/{UID}"
        response = await session.get(url)
        output = await response.json()
        if len(output) != 7:
            error = output[0]
            error = error[0]
            error = error["message"]
            return error
        else:
            return output


async def getUsersInfo(UIDs):
    output = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for UID in UIDs:
            tasks.append(session.get(f'https://users.roblox.com/v1/users/{UID}'))
        responses = await asyncio.gather(*tasks)
        for response in responses:
            output.append(await response.json())
        return output
