from app.db import postgre
from app.utils import chess

from app.utils import elo

def changeRating(user_id, blunder_id, success):
    if user_id is None:
        return None, None

    blunder = postgre.getBlunderById(blunder_id)
    if blunder is None:
        return None, None

    blunder_elo = blunder['elo']
    user_elo = postgre.getRating(user_id)

    newUserElo, newBlunderElo = elo.calculate(user_elo, blunder_elo, success)

    postgre.setRating(user_id, newUserElo)
    postgre.setRating(blunder_id, newBlunderElo)

    return newUserElo, (newUserElo - user_elo)

def getBlundersStatistics():
    return {
        'status': 'ok',
        'data': {
            'total-blunders-value' : postgre.countBlunders()
        }
    }

def getBlundersHistory(username, offset, limit):
    total = postgre.getBlunderHistoryCount(username)
    blunders = postgre.getBlundersHistory(username, offset, limit)

    result = []
    for blunder in blunders:
        blunder_info = postgre.getBlunderById(blunder['blunder_id'])
        fen = chess.blunderStartPosition(blunder_info['fen_before'], blunder_info['blunder_move'])

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
        blunder_info = postgre.getBlunderById(blunder['blunder_id'])
        fen = chess.blunderStartPosition(blunder_info['fen_before'], blunder_info['blunder_move'])

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

def getCommentsByUser(username, offset, limit):
    total = postgre.getCommentsByUserCount(username)
    comments = postgre.getCommentsByUser(username, offset, limit)

    result = {}
    for comment in comments:
        blunder_id = comment['blunder_id']

        blunder_info = postgre.getBlunderById(blunder_id)
        fen = chess.blunderStartPosition(blunder_info['fen_before'], blunder_info['blunder_move'])

        if blunder_id not in result:
            result[blunder_id] = {
                "blunder_id": blunder_id,
                "fen": fen,
                "comments": []
            }

        result[blunder_id]['comments'].append(
            {
                "date": comment['date'],
                "text": comment['text']
            }
        )

    return {
        'status': 'ok',
        'username': username,
        'data': {
            "total": total,
            "blunders": result
        }
    }
