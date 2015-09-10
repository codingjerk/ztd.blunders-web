from flask import jsonify, request

from app import app
from app.db import mongo, postgre
from app.utils import session, crossdomain

def gameShortInfo(data):
    whitePlayer = 'Unknown'
    whiteElo = '?'
    blackPlayer = 'Unknown'
    blackElo = '?'

    if data is not None:
        if 'White'    in data:
            whitePlayer = data['White']

        if 'WhiteElo' in data:
            whiteElo    = data['WhiteElo']

        if 'Black'    in data:
            blackPlayer = data['Black']

        if 'BlackElo' in data:
            blackElo    = data['BlackElo']

    return {
        'White': whitePlayer,
        'WhiteElo': whiteElo,
        'Black': blackPlayer,
        'BlackElo': blackElo,
    }

def getBlunderInfoById(blunder_id):
    blunder = postgre.getBlunderById(blunder_id)

    if blunder is None:
        return jsonify({
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

@app.route('/api/blunder/info', methods=['POST'])
@crossdomain.crossdomain()
def getBlunderInfo():
    try:
        blunder_id = request.json['blunder_id']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Blunder id required'
        })

    return getBlunderInfoById(blunder_id)

@app.route('/api/mobile/blunder/info', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def getBlunderInfoMobile():
    return getBlunderInfo()
