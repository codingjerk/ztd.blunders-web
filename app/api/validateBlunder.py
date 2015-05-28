import random
import json

from flask import request, jsonify

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
    try:
        blunder_id = request.json['id']
        userLine = request.json['line']
    except:
        return jsonify({
            'status': 'error',
            'message': 'Blunder id and user line required'
        })

    if session.isAnonymous(): return jsonify({'status': 'ok'})

    if not postgre.closeBlunderTask(session.username(), blunder_id): 
        return jsonify({
            'status': 'error', 
            'message': ''  # TODO: return warning to client
        })

    success = compareLines(blunder_id, userLine)

    blunder = mongo.getBlunderById(blunder_id)
    postgre.saveBlunderHistory(session.username(), blunder_id, blunder['elo'], success, userLine)

    newElo, delta = db.changeRating(session.username(), blunder_id, success)

    return jsonify({
        'status': 'ok',
        'elo': newElo, 
        'delta': delta
    })