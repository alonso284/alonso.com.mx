from flask import Flask, render_template, request, redirect, url_for, jsonify, Markup, session, Blueprint
import requests
import os
import json
from dotenv import load_dotenv
import base64
import psycopg2
from urllib.parse import urlparse



spotifySearch = Blueprint('spotifySearch', __name__,
                          static_folder='static', template_folder='templates')


# load URL to database parameters
load_dotenv() 
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

@spotifySearch.route('/', methods=['GET'])
def index():
    return render_template('spotifySearch.html')

# Admin Dashboard/ New playlist
@spotifySearch.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "GET":
        if 'username' in session and session['username'] == 'admin':

            print("Getting Database information")
            cursor.execute("SELECT * FROM playlists")
            selected = cursor.fetchall()

            PlaylistSet = []
            
            for playlist in selected:
                PlaylistSet.append({})
                PlaylistSet[-1]['ID'] = playlist[0]
                PlaylistSet[-1]['mood'] = playlist[1]
                PlaylistSet[-1]['description'] = playlist[2]
                PlaylistSet[-1]['status'] = requests.get(f'https://open.spotify.com/playlist/{playlist[0]}').status_code

            return render_template('admin.html', PlaylistSet=PlaylistSet)
        return redirect(url_for('spotifySearch.login'))
    else:
        print("Validating New Entry")
        if requests.get(f"https://open.spotify.com/playlist/{request.form['ID']}").status_code == 200:
            

            cursor.execute(
                f"SELECT * FROM playlists WHERE playlistID='{request.form['ID']}'")
            toEdit = cursor.fetchone()

            if toEdit == None:
                print("Entry Validated")
                cursor.execute(f"INSERT INTO playlists (playlistID, mood, description) VALUES ('{request.form['ID']}', '{'n'*12}', 'No Description');")
                conn.commit()
                return redirect(url_for('spotifySearch.adminEdit', playlistID = request.form['ID']))
        print("Entry Invalidated")
        return redirect(url_for('spotifySearch.admin'))

# Show individual Playlist
@spotifySearch.route('/admin/<playlistID>', methods=['GET', 'POST'])
def adminEdit(playlistID):
    if request.method == "POST":

        # Validate new MOOD requested
        for letter in request.form['mood']:
            if not(letter == 'n' or letter == 'A' or letter == 'B' or letter == 'C' or letter == 'D'):
                return redirect(url_for('spotifySearch.admin'))

        # Looking if playlist exists
        cursor.execute(
            f"SELECT * FROM playlists WHERE playlistID='{playlistID}'")
        playlist = cursor.fetchone()

        if playlist != None:
            print("Updating Playlist")
            # Update database
            cursor.execute(
                f"UPDATE playlists SET mood='{request.form['mood']}',  description = '{request.form['description']}' WHERE playlistID='{playlistID}';")
            conn.commit()
        else:
            print("Playlist Doesnt Exist")

        return redirect(url_for('spotifySearch.admin'))

    if 'username' in session and session['username'] == 'admin':

        cursor.execute(
            f"SELECT * FROM playlists WHERE playlistID='{playlistID}'")
        toEdit = cursor.fetchone()

        if toEdit != None:
            return render_template('adminEdit.html', playlist=toEdit)
    return redirect(url_for('spotifySearch.login'))

# Login page
@spotifySearch.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if (request.form['password'] == os.getenv("userAdmin") and request.form['username'] == "admin"):
            # Set session username to admin
            session['username'] = request.form['username']
            print("Logged in as " + session['username'])
        return redirect(url_for('spotifySearch.admin'))

    if 'admin' in session:
        return redirect(url_for('spotifySearch.admin'))
    return '''
        <form method="POST">
            <p><input type=text name=username></p>
            <p><input type=text name=password></p>
            <p><input type=submit value=Login></p>
        </form>
    '''


@spotifySearch.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('spotifySearch.login'))

@spotifySearch.route('/RemovePlaylist/<playlistID>')
def RemovePlaylist(playlistID):

    cursor.execute(
            f"DELETE FROM playlists WHERE playlistID='{playlistID}';")
    conn.commit()


    print("Deleted " + playlistID + "successfully")
    return redirect(url_for('spotifySearch.admin'))

@spotifySearch.route('/search', methods=['GET'])
def search():
    return render_template('search.html')


@spotifySearch.route('/results/<mood>', methods=['GET'])
def results(mood):

    cursor.execute("SELECT * FROM playlists")
    selected = cursor.fetchall()

    orderedPlaylists = []

    for r in selected:
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
    orderedPlaylists.sort()
    print((orderedPlaylists))

    return render_template('results.html', playlists=orderedPlaylists)
