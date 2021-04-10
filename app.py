from flask import Flask, render_template, request, redirect, url_for
import json
import random
import requests

app = Flask(__name__)
APP_KEY = "AIzaSyDOb-UeE7x6ZFawF9oWFmflSnRlUi3UA0k"


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
    return render_template('RCG/RCG.html', red=random.randint(0,255), blue=random.randint(0,255),green=random.randint(0,255),)

# @app.route('/Weather', methods=['GET'])
# def Weather():
#     myRequest = requests.get('https://api.openweathermap.org/data/2.5/weather?q=Merida&appid=d0f71e8be8c42b4f95e46122e9294681&units=metric').json()

#     return render_template('Weather/Weather.html', myRequest=myRequest)

@app.route('/Weather/<location>', methods=['GET'])
def WeatherLocation(location):
    myTemperature = requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&appid=d0f71e8be8c42b4f95e46122e9294681&units=metric'.format(location)).json()
    myPlace = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key={}&input={}&inputtype=textquery'.format(APP_KEY,location)).json()
    photoReference = requests.get('https://maps.googleapis.com/maps/api/place/details/json?key={}&place_id={}'.format(APP_KEY, myPlace["candidates"][0]["place_id"])).json()
    myImage = "https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth=800&maxheight=1000".format(APP_KEY,photoReference["result"]["photos"][0]["photo_reference"])
    return render_template('Weather/Weather.html', myTemperature=myTemperature, myImage = myImage)


# Authorization
@app.route('/google8d0bb958fcdde5c3.html', methods=['GET'])
def googleVerification():
    return render_template('google8d0bb958fcdde5c3.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
