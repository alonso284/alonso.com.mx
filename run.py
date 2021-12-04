from dotenv import load_dotenv
from flask import Flask, render_template, url_for
from flask_login import LoginManager
import os
from tools.tools import tools
from spotifySearch.spotifySearch import spotifySearch

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = os.getenv("FLASK_KEY").encode("utf-8")

app.register_blueprint(tools, url_prefix='/tools')
app.register_blueprint(spotifySearch, url_prefix='/spotifySearch')


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Microsoft Azure Vision
@app.route('/Azure', methods=['GET'])
def MicrosoftAzure():
    return "online"


# Authorization
@app.route('/google8d0bb958fcdde5c3.html', methods=['GET'])
def googleVerification():
    return render_template('google8d0bb958fcdde5c3.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
