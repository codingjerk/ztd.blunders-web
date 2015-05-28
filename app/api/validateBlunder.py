import random
import json

import flask
from flask import request

from app import app, db
from app.db import mongo, postgre
from app.utils import session

def compareLines(blunder_id, userLine):
    data = mongo.getBlunderById(blunder_id)
    if data == None: return
    
    originalLine = [data['blunderMove']] + data['forcedLine']

    # TODO: Compare using pychess
    return originalLine == userLine

@app.route('/validateBlunder', methods = ['POST'])
def validateBlunder():
    blunder_id = request.json['id']
    userLine = request.json['line']

    if session.isAnonymous(): return flask.jsonify({'status': 'ok'})

    if not postgre.closeBlunderTask(session.username(), blunder_id): 
        return flask.jsonify({
            'status': 'error', 
            'message': ''  # TODO: return warning to client
        })

    success = compareLines(blunder_id, userLine)
    newElo, delta = db.changeRating(session.username(), blunder_id, success)

    return flask.jsonify({
        'status': 'ok',
        'elo': newElo, 
        'delta': delta
    })