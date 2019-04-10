import requests

def get(endpoint, param={}):
    param["app"] = 3
    return requests.get("https://devrant.com/api" + endpoint, params=param).json()

def newestIds():
    rants = get("/devrant/rants", {"sort": "recent", "limit": 2})
    return [(rants["rants"][0]["id"], rants["rants"][0]["created_time"]), (rants["rants"][1]["id"], rants["rants"][1]["created_time"])]

def getRant(id):
    return get("/devrant/rants/" + str(id))