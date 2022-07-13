from flask import Flask, render_template, request, redirect, url_for, jsonify, Markup, session, Blueprint
import requests
import os
import base64
import psycopg2
from lxml.html import fromstring
from urllib.parse import urlparse

spotifySearch = Blueprint('spotifySearch', __name__,
                          static_folder='static', template_folder='templates')


@spotifySearch.route('/', methods=['GET'])
def index():
    return render_template('spotifySearch.html')


@spotifySearch.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "GET":
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

            return render_template('admin.html', playlists=results)
        return redirect(url_for('spotifySearch.login'))
    else:
        return redirect(url_for('spotifySearch.admin'))
        # get post request to add playlist
        # check if ID is valid, if it is, add it to de data base


@spotifySearch.route('/admin/<playlistID>', methods=['GET', 'POST'])
def adminEdit(playlistID):
    if request.method == "POST":
        print(request.form['mood'])
        print(request.form['description'])
        print(playlistID)

        for i in request.form['mood']:
            print(i)
            if not(i == 'n' or i == 'A' or i == 'B' or i == 'C' or i == 'D'):
                return redirect(url_for('spotifySearch.admin'))

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

        cursor.execute(
            f"UPDATE playlists SET mood='{request.form['mood']}',  description = '{request.form['description']}' WHERE playlistID='{playlistID}';")

        cursor.close()
        conn.commit()
        conn.close()

        return redirect(url_for('spotifySearch.admin'))

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

        cursor.execute(
            f"SELECT * FROM playlists WHERE playlistID='{playlistID}'")
        toEdit = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('adminEdit.html', playlist=toEdit[0])
    return redirect(url_for('spotifySearch.login'))


@spotifySearch.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == os.getenv("userAdmin"):
            session['username'] = request.form['username']

        return redirect(url_for('spotifySearch.admin'))

    if 'username' in session:
        return redirect(url_for('spotifySearch.admin'))
    return '''
        <form method="POST">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@spotifySearch.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('spotifySearch.login'))


@spotifySearch.route('/search', methods=['GET'])
def search():
    return render_template('search.html')


@spotifySearch.route('/results/<mood>', methods=['GET'])
def results(mood):

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

    return render_template('results.html', playlists=orderedPlaylists)
