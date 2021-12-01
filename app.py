from flask import Flask, render_template, request, redirect, url_for, jsonify, Markup, session
from flask_login import LoginManager
import json
import random
import requests
import os
import base64
import psycopg2
from urllib.parse import urlparse
from queue import PriorityQueue
from markupsafe import escape

# from dotenv import load_dotenv
# load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = os.getenv("FLASK_KEY").encode("utf-8")


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


# RANDOM WORD GENERATOR
@app.route('/RandomWordGenerator', methods=['GET'])
def RWG():
    return render_template('RWG/RWG.html')


@app.route('/RandomWordGenerator/word', methods=['GET'])
def RWGw():
    with open('./json/RWG/RandomWord.json') as myArr:
        randomWordArr = json.load(myArr)
    return render_template('RWG/RWGw.html', randomWord=random.choice(randomWordArr))


@app.route('/RandomWordGenerator/subadj', methods=['GET'])
def RWGsubadj():
    return render_template('RWG/RWGsubadj.html')

# RANDOM COLOR GENERATOR


@app.route('/RandomColorGenerator', methods=['GET'])
def RCG():
    return render_template('RCG/RCG.html', red=random.randint(0, 255), blue=random.randint(0, 255), green=random.randint(0, 255),)


@app.route('/Weather', methods=['GET', 'POST'])
def Weather():
    if request.method == 'GET':
        return render_template('Weather/WeatherForm.html')
    else:
        city = request.form['city']
        return redirect('/Weather/{}'.format(city))


# Weather App
@app.route('/Weather/<location>', methods=['GET'])
def WeatherLocation(location):
    try:
        myTemperature = requests.get(
            'https://api.openweathermap.org/data/2.5/weather?appid={}&q={}&units=metric'.format(os.getenv("OP_KEY"), location)).json()
        myPlace = requests.get(
            'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key={}&input={}&inputtype=textquery'.format(os.getenv("G_KEY"), location)).json()
        photoReference = requests.get('https://maps.googleapis.com/maps/api/place/details/json?key={}&place_id={}'.format(
            os.getenv("G_KEY"), myPlace["candidates"][0]["place_id"])).json()
        myImage = "https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth=800&maxheight=1000".format(
            os.getenv("G_KEY"), photoReference["result"]["photos"][0]["photo_reference"])
        return render_template('Weather/Weather.html', myTemperature=myTemperature, myImage=myImage)
    except:
        return render_template('Weather/WeatherForm.html', ErrorMessage="Oops, not a city, try again")


# TicTac-Toe
@app.route('/TicTac-Toe', methods=['GET'])
def TicTacToe():
    return render_template('TicTac-Toe/TicTac-Toe.html')


# spotifySearch
@app.route('/spotifySearch', methods=['GET'])
def spotifySearch():
    return render_template('spotifySearch/spotifySearch.html')


@app.route('/spotifySearch/admin', methods=['GET'])
def admin():
    if 'username' in session:
        result = urlparse(os.getenv("DATABASE_URL"))

        # connect to the db
        conn = psycopg2.connect(
            host=result.hostname,
            database=result.path[1:],
            user=result.username,
            password=result.password,
            port=result.port
        )
        # cursor
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM playlists")
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('spotifySearch/admin.html', playlists=results)
    return redirect(url_for('login'))


@app.route('/spotifySearch/admin/<mood>', methods=['GET'])
def adminEdit(mood):
    if 'username' in session:
        result = urlparse(os.getenv("DATABASE_URL"))

        # connect to the db
        conn = psycopg2.connect(
            host=result.hostname,
            database=result.path[1:],
            user=result.username,
            password=result.password,
            port=result.port
        )
        # cursor
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM playlists WHERE playlistID='{mood}'")
        toEdit = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('spotifySearch/adminEdit.html', playlist=toEdit[0])
    return redirect(url_for('login'))


@app.route('/spotifySearch/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == os.getenv("userAdmin"):
            session['username'] = request.form['username']

        return redirect(url_for('admin'))

    if 'username' in session:
        return redirect(url_for('admin'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/spotifySearch/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/spotifySearch/search', methods=['GET'])
def spotifySearch_search():
    return render_template('spotifySearch/search.html')


@app.route('/spotifySearch/result', methods=['GET'])
def spotifySearch_result():
    mood = request.args.get("mood")

    result = urlparse(os.getenv("DATABASE_URL"))

    # connect to the db
    conn = psycopg2.connect(
        host=result.hostname,
        database=result.path[1:],
        user=result.username,
        password=result.password,
        port=result.port
    )
    # cursor
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM playlists")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    orderedPlaylists = []

    for r in results:
        coincidence = 0
        total = 0
        for l in range(0, len(r[1])):
            if mood[l] != 'n' and r[1][l] != 'n':
                total += 1
                coincidence += (mood[l] == r[1][l])
        if(total == 0 or coincidence == 0):
            continue
        else:
            orderedPlaylists.append(
                (round((coincidence/total)*100), r))

    # return render_template('spotifySearch/results.html', playlists=json.dumps(orderedPlaylists))
    return render_template('spotifySearch/results.html', playlists=orderedPlaylists)


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
