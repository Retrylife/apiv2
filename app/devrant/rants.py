from flask import Flask, Blueprint
from output import respond
from .external import *

devrant_rants = Blueprint("devrant rants", __name__)

@devrant_rants.route("/devrant/info")
def info():
    ids = newestIds()
    id_diff = ids[0][0] - ids[1][0]
    time_diff = ids[0][1] - ids[1][1]

    return respond({"success": True, "newest_id": ids[0][0], "newest_time": ids[0][1], "id_gap": id_diff, "time_gap": time_diff})

@devrant_rants.route("/devrant/rants/<id>/people")
def tba(id):
    rant = getRant(id)

    try:
        users = [rant["rant"]["user_username"]]
    except:
        return respond({"success": False, "error":"Rant does not exsist"})

    for comment in rant["comments"]:
        users.append(comment["user_username"])

    return respond({"success": True, "users":users})
    