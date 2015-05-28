from flask import jsonify, request

import random

from app import app, db
from app.db import mongo, postgre
from app import utils
from app.utils import session

@app.route('/getBlunderInfo', methods=['POST'])
def getBlunderInfo():
    try:
        blunder_id = request.json['blunder_id']
    except:
        return jsonify({
            'status': 'error',
            'message': 'Blunder id required'
        })

    blunder = mongo.getBlunderById(blunder_id)

    if blunder is None: return jsonify({
        'status': 'error',
        'message': 'Invalid blunder id',
    })

    elo = blunder['elo']

    totalTries = random.randint(0, 1000) # TODO: get from postgre
    successTries = int(totalTries / 3)

    comments = [{
        'id': 1,
        'likes': 10,
        'dislikes': 1,
        'date': 'yesterday',
        'parent_id': 0,
        'username': 'JackalSh',
        'text': 'This position is the best i saw ever!',
    },{
        'id': 2,
        'likes': 1,
        'dislikes': 6,
        'date': 'yesterday',
        'parent_id': 1,
        'username': 'Failuref',
        'text': 'NOOOOOOO! THIS POSITION IS VERY BAD!!!',
    }] # TODO: get comments

    myFavorite = random.randint(0, 100) > 90

    favorites = random.randint(0, 100)
    likes = random.randint(0, 100)
    dislikes = random.randint(0, 100)
    
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