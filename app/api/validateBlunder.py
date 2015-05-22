import random
import json
from bson.objectid import ObjectId 

import flask
from flask import request, session

from app import app, db
from app.db import mongo, postgre

def compareLines(blunder_id, userLine):
    data = mongo.db['filtered_blunders'].find({'_id': ObjectId(blunder_id)})
    if data.count() != 1: return
    
    fen = data[0]['fenBefore']
    originalLine = [data[0]['blunderMove']] + data[0]['forcedLine']

    print(fen, originalLine, userLine)

    # TODO: Compare using pychess
    return originalLine == userLine

@app.route('/validateBlunder', methods = ['POST'])
def validateBlunder():
    blunder_id = request.json['id']
    userLine = request.json['line']

    if 'username' in session:
        # TODO: check if we have that task assigned

        postgre.closeBlunderTask(session['username'], blunder_id)

        success = compareLines(blunder_id, userLine)

        newElo, delta = db.changeRating(session['username'], blunder_id, success)

        return flask.jsonify({'elo': newElo, 'delta': delta})

    return flask.jsonify({})