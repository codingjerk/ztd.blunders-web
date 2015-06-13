from flask import jsonify, request

import random

from app import app, db
from app.db import mongo, postgre
from app import utils
from app.utils import session

def gameShortInfo(data):
    whitePlayer = 'Unknown'
    whiteElo = '?'
    blackPlayer = 'Unknown'
    blackElo = '?'

    if data is not None: 
        if 'White'    in data: whitePlayer = data['White']    
        if 'WhiteElo' in data: whiteElo    = data['WhiteElo'] 
        if 'Black'    in data: blackPlayer = data['Black']    
        if 'BlackElo' in data: blackElo    = data['BlackElo'] 

    return {
        'White': whitePlayer,
        'WhiteElo': whiteElo,
        'Black': blackPlayer,
        'BlackElo': blackElo,
    }

def getBlunderInfoById(blunder_id):
    blunder = mongo.getBlunderById(blunder_id)

    if blunder is None: return jsonify({
        'status': 'error',
        'message': 'Invalid blunder id',
    })

    elo = blunder['elo']

    successTries, totalTries = postgre.getTries(blunder_id)

    comments = postgre.getBlunderComments(blunder_id)
    myFavorite = postgre.isFavorite(session.userID(), blunder_id)
    favorites = postgre.getBlunderPopularity(blunder_id)
    likes, dislikes = postgre.getBlunderVotes(blunder_id)

    gameInfo = gameShortInfo(mongo.getGameById(blunder['pgn_id']))
    
    return jsonify({
        'status': 'ok',
        'data': {
            'elo': elo,
            'totalTries': totalTries,
            'successTries': successTries,
            'comments': comments,
            'myFavorite': myFavorite,
            'likes': likes,
            'dislikes': dislikes,
            'favorites': favorites,
            'game-info': gameInfo
        }
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