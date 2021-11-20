from flask import Flask, render_template, request, redirect, url_for
import json
import random
import requests
import os
import base64

# from dotenv import load_dotenv
# load_dotenv()  # take environment variables from .env.

app = Flask(__name__)


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
    # clientID = os.getenv("spotifyIDclient")
    # clientSECRET = os.getenv(("spotifySECRETclient"))

    # basic = clientID + ":" + clientSECRET
    # basic_bytes = basic.encode('ascii')
    # base_bytes = base64.b64encode(basic_bytes)
    # base = base_bytes.decode('ascii')

    # headers = {'Authorization': "Basic " + base,
    #            'Content-Type': 'application/x-www-form-urlencoded'}
    # body = {'grant_type': 'client_credentials'}

    # r = requests.post(
    #     'https://accounts.spotify.com/api/token', headers=headers, data=body)
    # print(r.text)

    # authKey = json.loads(r.text)['access_token']
    # return render_template('spotifySearch/spotifySearch.html', authKey=authKey)

    IDs = ["0XGoStPNhm6ak2wpaeANue",
           "3QpSL2PDMh2Nvo21IrODkb", "2V1aCYKF6MzdDuyxToaHmO"]

    return render_template('spotifySearch/spotifySearch.html', IDs=IDs)


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
