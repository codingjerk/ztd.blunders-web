
from flask import request, jsonify

from app import app, db
from app.db import mongo, postgre
from app.utils import session

from app.api.getBlunderInfo import getBlunderInfoById

@app.route('/voteBlunder', methods = ['POST'])
def voteBlunder():
    if session.isAnonymous(): return jsonify({
        'status': 'error',
        'message': 'Voting allowed only for authorized user'
    })

    try:
        blunder_id = request.json['blunder_id']
        vote = request.json['vote']
    except:
        return jsonify({
            'status': 'error',
            'message': 'Blunder id and vote required'
        })

    if not postgre.voteBlunder(session.userID(), blunder_id, vote): 
        return jsonify({
            'status': 'error', 
            'message': "Can't vote blunder"
        })

    return getBlunderInfoById(blunder_id)

@app.route('/favoriteBlunder', methods = ['POST'])
def favoriteBlunder():
    if session.isAnonymous(): return jsonify({
        'status': 'error',
        'message': 'Favorites allowed only for authorized user'
    })

    try:
        blunder_id = request.json['blunder_id']
    except:
        return jsonify({
            'status': 'error',
            'message': 'Blunder id required'
        })

    if not postgre.favoriteBlunder(session.userID(), blunder_id): 
        return jsonify({
            'status': 'error', 
            'message': "Can't favorite blunder"
        })

    return getBlunderInfoById(blunder_id)