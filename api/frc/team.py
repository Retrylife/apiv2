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

    return respond({"success": True, "data": {"team_key": data["key"], "name": data["nickname"], "website": data["website"], "country": data["country"]}})

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
        year = event["year"]
        if year not in event_keys:
            event_keys[year] = {}
        
        # Change null week to worlds
        if event["week"] == None:
            event["week"] = "worlds"
        
        # Set info
        event_keys[year][event["week"]] = event["key"]

    return respond({"success": True, "events": event_keys})
    
