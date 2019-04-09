
from flask import jsonify

def respond(data):
    res = jsonify(data)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res