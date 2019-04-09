from flask import Flask, Blueprint
from flask import jsonify
from .external import *

devrant_rants = Blueprint("devrant rants", __name__)

@devrant_rants.route("/devrant/info")
def info():
    ids = newestIds()
    id_diff = ids[0][0] - ids[1][0]
    time_diff = ids[0][1] - ids[1][1]

    return jsonify({"success": True, "newest_id": ids[0][0], "newest_time": ids[0][1], "id_gap": id_diff, "time_gap": time_diff})

@devrant_rants.route("/devrant/rants/<id>/people")
def tba(id):
    rant = getRant(id)

    users = [rant["rant"]["user_username"]]

    for comment in rant["comments"]:
        users.append(comment["user_username"])

    return jsonify({"success": True, "users":users})
    