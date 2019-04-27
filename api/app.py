from flask import Flask
from flask_cors import CORS
import html

# paths
from auth.tba import auth_tba
from devrant.rants import devrant_rants
from status import status
from frc.team import frc_teams
from databuffer.monitor import databuffer_monitor
from databuffer.buffer import cleaning_thread
from auth.keygen import auth_keygen
from frc.events import frc_events
from auth.devices.register import dev_reg

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
print("Registering endpoints")
register(auth_tba)
register(devrant_rants)
register(status)
register(frc_teams)
register(databuffer_monitor)
register(auth_keygen)
register(frc_events)
register(dev_reg)

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

# Start task threads
print("Starting tasks")
cleaning_thread.start()


if __name__ == '__main__':
    # Start webserver
    app.run(host='0.0.0.0')