from flask import request, jsonify

from app import app
from app.db import postgre
from app.utils import session, const

from app.utils import elo, crossdomain

def compareLines(blunder_id, userLine):
    data = postgre.blunder.getBlunderById(blunder_id)
    if data == None:
        return

    originalLine = [data['blunder_move']] + data['forced_line']

    # TODO: Compare using pychess
    return originalLine == userLine

def changeRating(user_id, blunder_id, success):
    if user_id is None:
        return None, None

    blunder = postgre.blunder.getBlunderById(blunder_id)
    if blunder is None:
        return None, None

    blunder_elo = blunder['elo']
    user_elo = postgre.user.getRating(user_id)

    newUserElo, newBlunderElo = elo.calculate(user_elo, blunder_elo, success)

    postgre.user.setRatingUser(user_id, newUserElo)
    postgre.blunder.setRatingBlunder(blunder_id, newBlunderElo)

    return newUserElo, (newUserElo - user_elo)

def validateExploreBlunder(blunder_id, userLine, spentTime): #pylint: disable=unused-argument
    postgre.blunder.closeBlunderTask(session.userID(), blunder_id, const.tasks.EXPLORE)

    return jsonify({'status': 'ok'})

def validateRatedBlunder(blunder_id, userLine, spentTime):
    if session.isAnonymous():
        return jsonify({'status': 'ok'})

    date_start = postgre.blunder.getTaskStartDate(session.userID(), blunder_id, const.tasks.RATED)

    if not postgre.blunder.closeBlunderTask(session.userID(), blunder_id, const.tasks.RATED):
        return jsonify({
            'status': 'error',
            'message': "Validation failed"
        })

    success = compareLines(blunder_id, userLine)

    blunder = postgre.blunder.getBlunderById(blunder_id)
    user_id = session.userID()
    user_elo = postgre.user.getRating(user_id)

    postgre.blunder.saveBlunderHistory(
        user_id,
        user_elo,
        blunder_id,
        blunder['elo'],
        success,
        userLine,
        date_start,
        spentTime
    )

    newElo, delta = changeRating(session.userID(), blunder_id, success)

    return jsonify({
        'data':{
            'elo': newElo,
            'delta': delta
            },
        'status': 'ok'
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

    if type == const.tasks.RATED:
        return validateRatedBlunder(blunder_id, userLine, spentTime)
    elif type == const.tasks.EXPLORE:
        return validateExploreBlunder(blunder_id, userLine, spentTime)
    else:
        return jsonify({
            'status': 'error',
            'message': 'Blunder type must be rated or explore'
        })

@app.route('/api/mobile/blunder/validate', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def validateBlunderMobile():
    return validateBlunder()
