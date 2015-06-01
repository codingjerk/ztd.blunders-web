from flask import jsonify, request

import random

from app import app, db
from app.db import mongo, postgre
from app import utils
from app.utils import session

def getBlunderInfoById(blunder_id):
    blunder = mongo.getBlunderById(blunder_id)

    if blunder is None: return jsonify({
        'status': 'error',
        'message': 'Invalid blunder id',
    })

    elo = blunder['elo']

    successTries, totalTries = postgre.getTries(blunder_id)

    comments = postgre.getBlunderComments(blunder_id)
    myFavorite = postgre.myFavorite(session.username(), blunder_id)
    favorites = postgre.getBlunderPopularity(blunder_id)
    likes, dislikes = postgre.getBlunderVotes(blunder_id)
    
    return jsonify({
        'status': 'ok',
        'elo': elo,
        'totalTries': totalTries,
        'successTries': successTries,
        'comments': comments,
        'myFavorite': myFavorite,
        'likes': likes,
        'dislikes': dislikes,
        'favorites': favorites,
    })


@app.route('/getBlunderInfo', methods=['POST'])
def getBlunderInfo():
    try:
        blunder_id = request.json['blunder_id']
    except:
        return jsonify({
            'status': 'error',
            'message': 'Blunder id required'
        })
        
    return getBlunderInfoById(blunder_id)

    