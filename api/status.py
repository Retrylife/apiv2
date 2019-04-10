from flask import Flask, Blueprint
from output import respond

status = Blueprint("api status", __name__)

@status.route("/status")
def tba():
    return respond({"success":True, "message":"I am alive!"})