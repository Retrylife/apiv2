from flask import Flask, Blueprint, request
from output import respond
from auth.keymanagement import access
import hashlib

auth_keygen = Blueprint("auth keygen", __name__)

@auth_keygen.route("/auth/keygen", methods=["GET"])
def keygen():
    api_key = request.args.get("key")
    if not api_key:
        return respond({"success": False, "error": "No Input Key Provided"})
    
    data = hashlib.sha512(api_key.encode()).hexdigest()

    return data