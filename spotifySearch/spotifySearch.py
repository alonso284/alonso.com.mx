from flask import Flask, render_template, request, redirect, url_for, jsonify, Markup, session, Blueprint
import requests
import os
import base64
import psycopg2
from urllib.parse import urlparse

spotifySearch = Blueprint('spotifySearch', __name__,
                          static_folder='static', template_folder='templates')


@spotifySearch.route('/', methods=['GET'])
def index():
    session['username'] = 'normal'
    return render_template('spotifySearch.html')


# Admin Dashboard/ New playlist
@spotifySearch.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "GET":
        if session['username'] == 'admin':
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

            status = []
            
            for i in results:
                status.append(requests.get(f'https://open.spotify.com/playlist/{i[0]}').status_code)
            print(status)


            return render_template('admin.html', playlists=results, status=status, len = len(results))
        return redirect(url_for('spotifySearch.login'))
    else:
        print("evaluating")
        if requests.get(f"https://open.spotify.com/playlist/{request.form['ID']}").status_code == 200:
            # Check if id exists in database
            # connect to the db
            result = urlparse(os.getenv("DATABASE_URL"))
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
                f"SELECT * FROM playlists WHERE playlistID='{request.form['ID']}'")
            toEdit = cursor.fetchall()

            if not toEdit:
                print("ABBLE TO INSERT")
                cursor.execute(f"INSERT INTO playlists (playlistID, mood, description) VALUES ('{request.form['ID']}', '{'n'*12}', 'No Description');")
                cursor.close()
                conn.commit()
                conn.close()
                return redirect(url_for('spotifySearch.adminEdit', playlistID = request.form['ID']))

            

            cursor.close()
            conn.close()

            

        return redirect(url_for('spotifySearch.admin'))

# Show individual Playlist
@spotifySearch.route('/admin/<playlistID>', methods=['GET', 'POST'])
def adminEdit(playlistID):
    if request.method == "POST":
        print(request.form['mood'])
        print(request.form['description'])
        print(playlistID)

        # Validate new MOOD
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

        # Update database
        cursor.execute(
            f"UPDATE playlists SET mood='{request.form['mood']}',  description = '{request.form['description']}' WHERE playlistID='{playlistID}';")

        cursor.close()
        conn.commit()
        conn.close()

        return redirect(url_for('spotifySearch.admin'))

    if session['username'] == "admin":
        print("user in session is admin")
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

# Login page
@spotifySearch.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if (request.form['password'] == os.getenv("userAdmin") and request.form['username'] == "admin"):
            # Set session username to admin
            session['username'] = request.form['username']
            print("login successful")
            print(session['username'])

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

    result = urlparse(os.getenv("DATABASE_URL"))
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
            f"DELETE FROM playlists WHERE playlistID='{playlistID}';")
    cursor.close()
    conn.commit()
    conn.close()
    print("Deleted " + playlistID + "successfully")
    return redirect(url_for('spotifySearch.admin'))



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
    orderedPlaylists.sort()
    print((orderedPlaylists))

    return render_template('results.html', playlists=orderedPlaylists)
