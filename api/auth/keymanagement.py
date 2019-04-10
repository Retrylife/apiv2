from .apikeys import read, all_scopes, internal_keys
from output import respond
import hashlib

def access(key, scope):
    key = hashlib.sha512(key.encode()).hexdigest()
    
    if key not in read:
        return True, respond({"success": False, "error": "API Key Invalid"})
    if not key:
        return True, respond({"success": False, "error": "No API Key Provided"})
    if scope not in all_scopes:
        return True, respond({"success": False, "error": "Invalid Scope Requested"})
    
    # get allowed scopes
    scopes = read[key]

    output = {}
    for scpoe in all_scopes:
        if scope in scopes:
            output[scope] = internal_keys[scope]
        else:
            output[scope] = None
    
    return False, output
    