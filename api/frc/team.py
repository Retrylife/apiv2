from flask import Flask, Blueprint, request
from output import respond
import requests
from auth.keymanagement import access
from databuffer.buffer import inquire

frc_teams = Blueprint("FRC teams", __name__)

@frc_teams.route("/frc/teams/<team>", methods=["GET"])
def teams(team):
    api_key = request.args.get("api-key")
    if not api_key:
        return respond({"success": False, "error": "No API Key Provided"})
    
    # Rewuest a tba key from keymanagement
    err, resp = access(api_key, "tba")
    if err:
        return resp
    
    tba_key = resp["tba"]
    
    data = inquire(f"https://www.thebluealliance.com/api/v3/team/frc{team}", headers={"X-TBA-Auth-Key":tba_key}).json()

    return respond({"success": True, "data": data})

@frc_teams.route("/frc/teams/<team>/simple", methods=["GET"])
def simpleTeams(team):
    api_key = request.args.get("api-key")
    if not api_key:
        return respond({"success": False, "error": "No API Key Provided"})
    
    # Rewuest a tba key from keymanagement
    err, resp = access(api_key, "tba")
    if err:
        return resp
    
    tba_key = resp["tba"]
    
    data = inquire(f"https://www.thebluealliance.com/api/v3/team/frc{team}", headers={"X-TBA-Auth-Key":tba_key}).json()

    return respond({"success": True, "team_key": data["key"], "name": data["nickname"], "website": data["website"], "country": data["country"]})

@frc_teams.route("/frc/teams/<team>/events", methods=["GET"])
def teamEvents(team):
    api_key = request.args.get("api-key")
    if not api_key:
        return respond({"success": False, "error": "No API Key Provided"})
    
    # Rewuest a tba key from keymanagement
    err, resp = access(api_key, "tba")
    if err:
        return resp
    
    tba_key = resp["tba"]
    
    data = inquire(f"https://www.thebluealliance.com/api/v3/team/frc{team}/events", headers={"X-TBA-Auth-Key": tba_key}).json()
    event_keys = {}
    for event in data:
        # Add years to output
        year = str(event["year"])
        if year not in event_keys:
            event_keys[year] = {}
        
        # Change null week to worlds
        if event["week"] == None:
            event["week"] = "worlds"
        
        # Set info
        event_keys[year][str(event["week"])] = event["key"]

    latest = event_keys[list(event_keys.keys())[-1]]
    latest = latest[list(latest.keys())[0]]

    return respond({"success": True, "events": event_keys, "latest":latest})
    
@frc_teams.route("/frc/teams/<team>/latest")
def teamLatest(team):
    api_key = request.args.get("api-key")
    if not api_key:
        return respond({"success": False, "error": "No API Key Provided"})
    
    # Rewuest a tba key from keymanagement
    err, resp = access(api_key, "tba")
    if err:
        return resp
    
    tba_key = resp["tba"]

    # Get current game year from TBA
    game_year = inquire(f"https://www.thebluealliance.com/api/v3/status", headers={"X-TBA-Auth-Key": tba_key}).json()["current_season"]

    data = inquire(f"https://www.thebluealliance.com/api/v3/team/frc{team}/events/{game_year}/statuses", headers={"X-TBA-Auth-Key": tba_key}).json()

    try:
        last_match = data[list(data)[0]]["last_match_key"]
        next_match = data[list(data)[0]]["next_match_key"]
    except:
        last_match = None
        next_match = None

    win = 0
    loss = 0
    tie = 0
    
    for event in data:
        event = data[event]
        if event["qual"] != None:
            win += event["qual"]["ranking"]["record"]["wins"]
            loss += event["qual"]["ranking"]["record"]["losses"]
            tie += event["qual"]["ranking"]["record"]["ties"]
        if event["qual"] != None:
            win += event["playoff"]["record"]["wins"]
            loss += event["playoff"]["record"]["losses"]
            tie += event["playoff"]["record"]["ties"]
    
    wlt_str = "winning" if win > loss + tie else "loosing"

    rank = 0
    try:
        if data[list(data)[0]]["qual"] != None:
            rank += data[list(data)[0]]["qual"]["ranking"]["rank"]
    except:
        rank = 0
    
    last_match_data = {}
    if last_match != None:
        match_data = inquire(f"https://www.thebluealliance.com/api/v3/match/{last_match}/simple", headers={"X-TBA-Auth-Key": tba_key}).json()
        last_match_data["blue"] = {
            "score": match_data["alliances"]["blue"]["score"],
            "teams": [int(key[3:]) for key in match_data["alliances"]["blue"]["team_keys"]]
        }

        last_match_data["red"] = {
            "score": match_data["alliances"]["red"]["score"],
            "teams": [int(key[3:]) for key in match_data["alliances"]["red"]["team_keys"]]
        }
    else:
        last_match_data = None
    
    next_match_data = {}
    if next_match != None:
        match_data = inquire(f"https://www.thebluealliance.com/api/v3/match/{next_match}/simple", headers={"X-TBA-Auth-Key": tba_key}).json()
        next_match_data["blue"] = {
            "score": match_data["alliances"]["blue"]["score"],
            "teams": [int(key[3:]) for key in match_data["alliances"]["blue"]["team_keys"]]
        }

        next_match_data["red"] = {
            "score": match_data["alliances"]["red"]["score"],
            "teams": [int(key[3:]) for key in match_data["alliances"]["red"]["team_keys"]]
        }
    else:
        next_match_data = None

    latest_event = list(data)[0]

    power_data = inquire(f"https://www.thebluealliance.com/api/v3/event/{latest_event}/oprs", headers={"X-TBA-Auth-Key": tba_key}).json()
    opr = power_data["oprs"][f"frc{team}"]
    dpr = power_data["dprs"][f"frc{team}"]

    power_string = "offensive" if opr >= dpr else "defensive"

    picker_string = "picker" if rank <= 8 and rank != 0 else f"top {round(rank * 0.1)}0"

    return respond({"success": True, "next_match": next_match_data, "last_match": last_match_data, "wlt": [win, loss, tie], "wlt_string": wlt_str, "event_rank": rank, "opr":opr, "dpr": dpr, "opr_string": power_string, "rank_string": picker_string})