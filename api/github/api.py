import requests

def getProjects(user):
    return requests.get(f"https://api.github.com/users/{user}/repos").json()