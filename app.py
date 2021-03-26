from flask import Flask, render_template, request, redirect, url_for
import json
import random

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/RandomWordGenerator', methods=['GET'])
def RWG():
    with open('./json/RandomWord.json') as myArr:
        randomWordArr = json.load(myArr)
    return render_template('randomWord.html', randomWord=random.choice(randomWordArr))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
