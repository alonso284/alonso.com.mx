from flask import Flask, render_template, request, redirect, url_for
import json
import random

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
    return render_template('RCG/RCG.html', red=random.randint(0,255), blue=random.randint(0,255),green=random.randint(0,255),)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
