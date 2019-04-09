from flask import Flask, Blueprint
from flask import jsonify

auth_tba = Blueprint("tba auth", __name__)

@auth_tba.route("/auth/tba")
def tba():
    return jsonify({"success":True, "key":"QPI1VLcQrowB0Oq8G0NdTjk30HpSaJ4fJuO4GV29ATKJkJIS6GNVZ1qnlLg0O6Ql"})