from flask import Flask, Blueprint, request
from output import respond
from auth.keymanagement import access
from .data import buffered_urls, timeout

databuffer_monitor = Blueprint("RetryLife Databuffer Monitoring", __name__)

@databuffer_monitor.route("/databuffer/monitor", methods=["GET"])
def monitor():
    api_key = request.args.get("api-key")
    if not api_key:
        return respond({"success": False, "error": "No API Key Provided"})
    
    # Rewuest a tba key from keymanagement
    err, resp = access(api_key, "monitor")
    if err:
        return resp

    buffered = ""

    for item in buffered_urls:
        # rps = round(item["request_times"][1] - item["request_times"][0], 2)
        # rps = 1/rps
        buffered += f"<br>{item['url']}"
    
    data = f"""
    --- RetryLife Databuffer Monitor ---
    <br><br>
    Timeout: {timeout} seconds
    <br><br>
    Currently buffered resources:
    {buffered}
    """

    return data

@databuffer_monitor.route("/databuffer/monitor/json", methods=["GET"])
def monitorJson():
    api_key = request.args.get("api-key")
    if not api_key:
        return respond({"success": False, "error": "No API Key Provided"})
    
    # Rewuest a tba key from keymanagement
    err, resp = access(api_key, "monitor")
    if err:
        return resp

    urls = []

    for item in buffered_urls:
        urls.append(item['url'])

    return respond({"success":True, "timeout":timeout, "urls":urls})