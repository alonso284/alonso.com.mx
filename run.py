from dotenv import load_dotenv
from flask import Flask, render_template, url_for, session
from flask_login import LoginManager
import os
from tools.tools import tools
from spotifySearch.spotifySearch import spotifySearch
from impossibleHangman.impossibleHangman import impossibleHangman

# take environment variables from .env
load_dotenv()  

# Initiate App
app = Flask(__name__)

# Initialize Login Manager
login_manager = LoginManager()
# Configure for Login
login_manager.init_app(app)

# Set Scret Key
app.secret_key = os.getenv("FLASK_KEY").encode("utf-8")

# Load Tools App
app.register_blueprint(tools, url_prefix='/tools')
# Load Spotify Search App
app.register_blueprint(spotifySearch, url_prefix='/spotifySearch')
app.register_blueprint(impossibleHangman, url_prefix='/impossibleHangman')

# This callback is used to reload the user object from the user ID stored in the session. It should take the str ID of a user, and return the corresponding user object.
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Main Page/About Me
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Microsoft Azure Vision
@app.route('/Azure', methods=['GET'])
def MicrosoftAzure():
    return "online"


# Authorization for Google
@app.route('/google8d0bb958fcdde5c3.html', methods=['GET'])
def googleVerification():
    return render_template('google8d0bb958fcdde5c3.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
