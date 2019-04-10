#### External imports #####
from flask import Flask
from flask_cors import CORS
from output import respond
###########################

## Internal Routes ##

#####################

## Routing table ##

routing_table = {
    "/":[index, ["GET"], ["KEYLESS"]]
}

###################

## Router ##

@app.route("/<path:path>")
def router(path):
    # convert path to 
    # Error out of invalid path
    if parsed_path not in routing_table:
        return respond({"success": False, "error": "Invalid Endpoint"})
    


############