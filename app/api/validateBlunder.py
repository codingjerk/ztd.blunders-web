from flask import request, jsonify

from app import app, db
from app.db import mongo, postgre
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

@app.route('/validateBlunder', methods = ['POST'])
def validateBlunder():
    try:
        blunder_id = request.json['id']
        userLine = request.json['line']
        spentTime = request.json['spentTime']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Blunder id, user line and spent time required'
        })

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
