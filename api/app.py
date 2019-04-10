from flask import Flask
from flask_cors import CORS
import html

# paths
from auth.tba import auth_tba
from devrant.rants import devrant_rants
from status import status
from frc.team import frc_teams

app = Flask(__name__)
CORS(app)

# Blueprint registration
blueprints = []

def register(blueprint):
    app.register_blueprint(blueprint)
    blueprints.append(blueprint)

def getUrls(blueprint):
    temp_app = Flask(__name__) 
    temp_app.register_blueprint(blueprint)
    return [str(p) for p in temp_app.url_map.iter_rules()]

# Set up blueprints
register(auth_tba)
register(devrant_rants)
register(status)
register(frc_teams)

@app.route('/')
def index():
    return """
    Welcome to the RetryLife api v2.
    <br>
    This is a dark and mysterious place.
    """

@app.route("/endpoints")
def endpoints():
    # Return a list of all endpoints
    output = "Avalible API endpoints:"
    for blueprint in blueprints:
        for url in getUrls(blueprint):
            if url[:7] == "/static":
                continue
            output += f"<br><b>\t{html.escape(url)}</b>"
    return output


if __name__ == '__main__':
    app.run(host='0.0.0.0')