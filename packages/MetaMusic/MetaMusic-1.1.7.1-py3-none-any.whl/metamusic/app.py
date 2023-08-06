from flask import Flask, request, render_template, jsonify, abort
import multiprocessing
from multiprocessing import Pool
import time
import os
import numpy as np
import sys
import urllib
import webbrowser
import string
import glob
import random
from metamusic.fetcher import process_init
from metamusic.model import db, fetcher_database
import random

from pathlib import Path

import os

app = Flask(__name__, static_folder="./static/dist",
            template_folder="./static")
database_name = ''.join(random.choices(
    string.ascii_uppercase, k=10))
db_path = os.path.join(Path.home(), '.metamusic')
if not os.path.exists(db_path):
    os.mkdir(db_path)
for i in glob.glob(os.path.join(db_path, '*.db')):
    os.remove(i)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    db_path + '/' + database_name + '.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "thisisyunik"
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/process", methods=["GET"])
def process():
    path = request.args['path']
    if not os.path.exists(path):
        time.sleep(.3)
        return render_template("nofile.html")
    total_songs = 0
    if not os.path.isfile(path):
        p = Pool()
        folders = []
        for root, dirs, files in os.walk(path):

            results = p.map(f, files)
            numbers = np.sum(np.array(results) > 0)
            if numbers:
                folders.append(root)
            total_songs += numbers
        p.close()
        p.join()
        t = multiprocessing.Process(
            target=process_init, args=(path, app, db, folders))
    else:
        total_songs = 1
        folders = [os.path.dirname(path)]
        t = multiprocessing.Process(
            target=process_init, args=(path, app, db, folders))
    t.daemon = True
    t.start()
    time.sleep(0.4)
    return render_template("process.html", totalsongs=total_songs)


@app.route('/fetch/<int:no>')
def fetch(no):
    return_data = fetcher_database.query.filter_by(uid=no).first()
    while return_data is None:
        time.sleep(0.01)
        return_data = fetcher_database.query.filter_by(uid=no).first()
    if not return_data.status:
        return abort(404)
    return jsonify(trackname=return_data.trackname, tracknumber=return_data.tracknumber, albumname=return_data.albumname, image_url=return_data.image_url, releasedate=return_data.releasedate,
                   genre=return_data.genre, artistname=return_data.artistname, uid=return_data.uid, loading=True)


def f(n):
    if (n.endswith('.mp3')):
        return 1
    else:
        return 0


@app.errorhandler(404)
def page_not_found(e):
    return render_template("nofile.html")


def run():
    if len(sys.argv) >= 2:
        if os.path.exists(sys.argv[1]):
            path = os.path.abspath(sys.argv[1])
            if os.path.isdir(path):
                url = 'http://127.0.0.1:5999/process?path=' + \
                    urllib.parse.quote_plus(path)
                webbrowser.open(url)
                app.run(threaded=True)
            else:
                folders = [os.path.dirname(path)]
                process_init(path, app, db, folders)
        else:
            raise ValueError("The path/ file you entered doesn't exit")
    else:
        webbrowser.open('http://127.0.0.1:5999/')
        app.run(threaded=True,  host='0.0.0.0',port=5999)
