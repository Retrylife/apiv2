from flask import Flask, Blueprint, request
from output import respond
import requests
from auth.keymanagement import access
from databuffer.buffer import inquire

frc_events = Blueprint("FRC events", __name__)

@frc_events.route("/frc/events/<event>/twitch", methods=["GET"])
def webcast(event):
    api_key = request.args.get("api-key")
    if not api_key:
        return respond({"success": False, "error": "No API Key Provided"})
    
    # Rewuest a tba key from keymanagement
    err, resp = access(api_key, "tba")
    if err:
        return resp
    
    tba_key = resp["tba"]
    
    data = inquire(f"https://www.thebluealliance.com/api/v3/event/{event}", headers={"X-TBA-Auth-Key": tba_key}).json()
    
    streams = []

    for cast in data["webcasts"]:
        if cast["type"] == "twitch":
            streams.append(cast["channel"])

    return respond({"success": True, "livestreams": streams})
