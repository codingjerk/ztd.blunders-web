from flask import request, jsonify

from app import app, db
from app.db import mongo, postgre
from app.utils import session, tasks

def compareLines(blunder_id, userLine):
    data = mongo.getBlunderById(blunder_id)
    if data == None:
        return

    originalLine = [data['blunderMove']] + data['forcedLine']

    # TODO: Compare using pychess
    return originalLine == userLine

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

    blunder = mongo.getBlunderById(blunder_id)

    postgre.saveBlunderHistory(
        session.userID(),
        blunder_id,
        blunder['elo'],
        success,
        userLine,
        date_start,
        spentTime
    )

    newElo, delta = db.changeRating(session.userID(), blunder_id, success)

    return jsonify({
        'status': 'ok',
        'elo': newElo,
        'delta': delta
    })
