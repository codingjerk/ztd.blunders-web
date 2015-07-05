from flask import request, jsonify

from app import app
from app.db import postgre
from app.utils import session, tasks

from app.utils import elo

def compareLines(blunder_id, userLine):
    data = postgre.getBlunderById(blunder_id)
    if data == None:
        return

    originalLine = [data['blunder_move']] + data['forced_line']

    # TODO: Compare using pychess
    return originalLine == userLine

def changeRating(user_id, blunder_id, success):
    if user_id is None:
        return None, None

    blunder = postgre.getBlunderById(blunder_id)
    if blunder is None:
        return None, None

    blunder_elo = blunder['elo']
    user_elo = postgre.getRating(user_id)

    newUserElo, newBlunderElo = elo.calculate(user_elo, blunder_elo, success)

    postgre.setRatingUser(user_id, newUserElo)
    postgre.setRatingBlunder(blunder_id, newBlunderElo)

    return newUserElo, (newUserElo - user_elo)

def validateExploreBlunder(blunder_id, userLine, spentTime): #pylint: disable=unused-argument
    postgre.closeBlunderTask(session.userID(), blunder_id, tasks.EXPLORE)

    return jsonify({'status': 'ok'})

def validateRatedBlunder(blunder_id, userLine, spentTime):
    if session.isAnonymous():
        return jsonify({'status': 'ok'})

    date_start = postgre.getTaskStartDate(session.userID(), blunder_id, tasks.RATED)

    if not postgre.closeBlunderTask(session.userID(), blunder_id, tasks.RATED):
        return jsonify({
            'status': 'error',
            'message': "Validation failed"
        })

    success = compareLines(blunder_id, userLine)

    blunder = postgre.getBlunderById(blunder_id)

    postgre.saveBlunderHistory(
        session.userID(),
        blunder_id,
        blunder['elo'],
        success,
        userLine,
        date_start,
        spentTime
    )

    newElo, delta = changeRating(session.userID(), blunder_id, success)

    return jsonify({
        'status': 'ok',
        'elo': newElo,
        'delta': delta
    })

@app.route('/api/blunder/validate', methods = ['POST'])
def validateBlunder():
    try:
        blunder_id = request.json['id']
        userLine = request.json['line']
        spentTime = request.json['spentTime']
        type = request.json['type']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Blunder id, user line, spent time and type required'
        })

    if type == tasks.RATED:
        return validateRatedBlunder(blunder_id, userLine, spentTime)
    elif type == tasks.EXPLORE:
        return validateExploreBlunder(blunder_id, userLine, spentTime)
    else:
        return jsonify({
            'status': 'error',
            'message': 'Blunder type must be rated or explore'
        })