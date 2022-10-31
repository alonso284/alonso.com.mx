from flask import Flask, render_template, request, redirect, url_for, jsonify, Markup, session, Blueprint
import requests
import os
import random
import json
from dotenv import load_dotenv


# load URL to database parameters
load_dotenv()

tools = Blueprint('tools', __name__,
                  static_folder='static', template_folder='templates')


# RANDOM WORD GENERATOR
@tools.route('/RandomWordGenerator', methods=['GET'])
def RWG():
    return render_template('RWG/RWG.html')


@tools.route('/RandomWordGenerator/word', methods=['GET'])
def RWGw():
    with open('./tools/static/data/RWG/randomWords.json') as myArr:
        randomWordArr = json.load(myArr)
    return render_template('RWG/RWGw.html', randomWord=random.choice(randomWordArr))


@tools.route('/RandomWordGenerator/subadj/<numberOfAdjectives>', methods=['GET'])
def RWGsubadj(numberOfAdjectives):
    with open('./tools/static/data/RWG/randomAdjectives.json') as myArr:
        randomAjdArr = json.load(myArr)

    numberOfAdjectives = int(numberOfAdjectives)
    adjectives = []
    for i in range(numberOfAdjectives):
        adjectives.append(random.choice(randomAjdArr))

    return render_template('RWG/RWGsubadj.html', adjectives=adjectives)


# RANDOM COLOR GENERATOR
@tools.route('/RandomColorGenerator', methods=['GET'])
def RCG():
    return render_template('RCG/RCG.html', red=random.randint(0, 255), blue=random.randint(0, 255), green=random.randint(0, 255),)


# Weather
@tools.route('/Weather', methods=['GET', 'POST'])
def Weather():
    if request.method == 'GET':
        return render_template('Weather/WeatherForm.html')
    else:
        return redirect(url_for('tools.WeatherLocation', location=request.form['city']))


@tools.route('/Weather/<location>', methods=['GET'])
def WeatherLocation(location):
    try:
        myTemperature = requests.get(
            'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(location, os.getenv("OP_KEY"))).json()
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
@tools.route('/TicTacToe', methods=['GET'])
def TicTacToe():
    return render_template('TicTacToe/TicTacToe.html')
