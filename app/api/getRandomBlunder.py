import random

import flask
from flask import session

from app import app, db
from app.db import mongo
from app.db import postgre

def jsonifyBlunder(data):
    return {
        'id': str(data['_id']),
        'pgn_id': str(data['pgn_id']),
        'move_index': data['move_index'],

        'forcedLine': data['forcedLine'],
        'pv': data['pv'],

        'fenBefore': data['fenBefore'],
        'blunderMove': data['blunderMove'],

        'elo': data['elo'],
    }

def newBlunder():
    randomIndex = random.randrange(0, mongo.db['filtered_blunders'].count())

    data = mongo.db['filtered_blunders'].find().skip(randomIndex).limit(1)[0]

    if 'username' in session:
        postgre.assignBlunderTask(session['username'], str(data['_id']))

    return data

@app.route('/getRandomBlunder')
def getRandomBlunder():
    blunder = db.getAssignedBlunder(session['username'] if 'username' in session else None)

    if blunder is None:
        blunder = newBlunder()

    return flask.jsonify(jsonifyBlunder(blunder))