from flask import Flask, Blueprint, request
from output import respond
import requests
from auth.keymanagement import access
from databuffer.buffer import inquire

mpm_ical = Blueprint("MPM ical", __name__)

@mpm_ical.route("/rss/mpm2d1.xml", methods=["GET"])
def teams():
    
    data = inquire(f"https://calendar.google.com/calendar/ical/gotvdsb.ca_classroom525e4a2a%40group.calendar.google.com/public/basic.ics").text
    events = data.split("BEGIN:VEVENT")[1:]

    for event in events:
        print(event)

    return respond({"success": True, "data": data})