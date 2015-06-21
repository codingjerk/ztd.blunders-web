from app.db import mongo, postgre
from app.utils import chess

from app.utils import elo

def changeRating(user_id, blunder_id, success):
    if user_id is None: return

    blunder = mongo.getBlunderById(blunder_id)
    if blunder is None: return

    blunder_elo = blunder['elo']
    user_elo = postgre.getRating(user_id)

    newUserElo, newBlunderElo = elo.calculate(user_elo, blunder_elo, success)

    postgre.setRating(user_id, newUserElo)
    mongo.setRating(blunder_id, newBlunderElo)

    return newUserElo, (newUserElo - user_elo)

def getAssignedBlunder(user_id, type):
    if user_id is None: return None

    blunder_id = postgre.getAssignedBlunder(user_id, type)

    if blunder_id is None: return None

    return mongo.getBlunderById(blunder_id)

def getBlundersStatistics():
    return {
        'status': 'ok',
        'data': {
            'total-blunders-value' : mongo.countBlunders()
        }
    }

def getGameByBlunderId(blunder_id):
    blunder = mongo.getBlunderById(blunder_id)

def getBlundersHistory(username, offset, limit):
    total = postgre.getBlunderHistoryCount(username)
    blunders = postgre.getBlundersHistory(username, offset, limit)

    result = []
    for blunder in blunders:
        blunder_info = mongo.getBlunderById(blunder['blunder_id'])
        fen = chess.blunderStartPosition(blunder_info['fenBefore'], blunder_info['blunderMove'])

        result.append({
            "blunder_id": blunder['blunder_id'],
            "fen": fen,
            "result": blunder['result'],
            "date_start": blunder['date_start'],
            "spent_time": blunder['spent_time']
        })

    return {
        'status': 'ok',
        'username': username,
        'data': {
            "total": total,
            "blunders": result
        }
    }

def getBlundersFavorites(username, offset, limit):
    total = postgre.getBlunderFavoritesCount(username)
    blunders = postgre.getBlundersFavorites(username, offset, limit)

    result = []
    for blunder in blunders:
        blunder_info = mongo.getBlunderById(blunder['blunder_id'])
        fen = chess.blunderStartPosition(blunder_info['fenBefore'], blunder_info['blunderMove'])

        result.append({
            "blunder_id": blunder['blunder_id'],
            "fen": fen,
            "assign_date": blunder['assign_date']
        })

    return {
        'status': 'ok',
        'username': username,
        'data': {
            "total": total,
            "blunders": result
        }
    }
