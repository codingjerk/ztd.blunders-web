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
        if 'white' in data and data['white'] is not None:
            whitePlayer = data['white']

        if 'white_elo' in data and data['white_elo'] is not None:
            whiteElo    = data['white_elo']

        if 'black' in data and data['black'] is not None:
            blackPlayer = data['black']

        if 'black_elo' in data and data['black_elo'] is not None:
            blackElo    = data['black_elo']

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
    myVote = postgre.getUserVote(session.userID(), blunder_id)
    favorites = postgre.getBlunderPopularity(blunder_id)
    likes, dislikes = postgre.getBlunderVotes(blunder_id)

    gameInfo = gameShortInfo(postgre.getGameById(blunder['game_id']))

    return jsonify({
        'status': 'ok',
        'data': {
            'elo': elo,
            'totalTries': totalTries,
            'successTries': successTries,
            'comments': comments,
            'myFavorite': myFavorite,
            'myVote': myVote,
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
