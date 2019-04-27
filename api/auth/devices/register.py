
from flask import Flask, Blueprint, request
from output import respond
from .devices import devices
import time
from auth.keymanagement import access

dev_reg = Blueprint("Device Registraion", __name__)

@dev_reg.route("/auth/devices/register/<id>", methods=["GET"])
def register(id):
    devices[id] = {"registration_time": time.time()}

    return respond({"success": True})

@dev_reg.route("/auth/devices/unregister/<id>", methods=["GET"])
def unRegister(id):
    del devices[id]

    return respond({"success": True})

@dev_reg.route("/auth/devices/monitor/json", methods=["GET"])
def monitorJson():
    api_key = request.args.get("api-key")
    if not api_key:
        return respond({"success": False, "error": "No API Key Provided"})
    
    # Rewuest a tba key from keymanagement
    err, resp = access(api_key, "monitor")
    if err:
        return resp
    return respond({"success": True, "devices": devices})

@dev_reg.route("/auth/devices/monitor", methods=["GET"])
def monitor():
    api_key = request.args.get("api-key")
    if not api_key:
        return respond({"success": False, "error": "No API Key Provided"})
    
    # Rewuest a tba key from keymanagement
    err, resp = access(api_key, "monitor")
    if err:
        return resp

    devs = ""
    for item in devices:
        devs += f"<br>{item}: {devices[item]}"
    
    data = f"""
    --- RetryLife Registered Devices Monitor ---
    <br><br>
    Currently registered devices:
    {devs}
    """
    return data