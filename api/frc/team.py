from flask import Flask, Blueprint, request
from output import respond
import requests
from auth.keymanagement import access

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
    
    data = requests.get(f"https://www.thebluealliance.com/api/v3/team/frc{team}", headers={"X-TBA-Auth-Key":tba_key}).json()

    return respond({"success": True, "data":data})
