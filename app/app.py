from flask import Flask
from flask_cors import CORS

# paths
from auth.tba import auth_tba
from devrant.rants import devrant_rants

app = Flask(__name__)
CORS(app)

# Set up blueprints
app.register_blueprint(auth_tba)
app.register_blueprint(devrant_rants)

@app.route('/')
def index():
    return """
    Welcome to the RetryLife api v2.
    <br>
    This is a dark and mysterious place.
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0')