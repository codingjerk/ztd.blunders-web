from flask import request, jsonify

from app import app
from app.db import postgre
from app.utils import session, const

from app.utils import elo, crossdomain

def compareLines(blunder_id, user_line):
    data = postgre.blunder.getBlunderById(blunder_id)
    if data == None:
        return

    originalLine = [data['blunder_move']] + data['forced_line']

    # TODO: Compare using pychess
    return originalLine == user_line

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

def validate(blunder_id, user_line, spent_time, task_type):
    date_start = postgre.blunder.getTaskStartDate(session.userID(), blunder_id, task_type)

    if not postgre.blunder.closeBlunderTask(session.userID(), blunder_id, task_type):
        return jsonify({
            'status': 'error',
            'message': "Validation failed"
        })
    success = compareLines(blunder_id, user_line)

    blunder = postgre.blunder.getBlunderById(blunder_id)
    user_id = session.userID()
    user_elo = postgre.user.getRating(user_id)

    postgre.blunder.saveBlunderHistory(
        user_id,
        user_elo,
        blunder_id,
        blunder['elo'],
        success,
        user_line,
        date_start,
        spent_time
    )

    newElo, delta = changeRating(session.userID(), blunder_id, success)

    return {
        'data':{
            'elo': newElo,
            'delta': delta
            },
        'status': 'ok'
    }

def validateExploreBlunder(blunder_id, user_line, spent_time): #pylint: disable=unused-argument
    postgre.blunder.closeBlunderTask(session.userID(), blunder_id, const.tasks.EXPLORE)

    return jsonify({'status': 'ok'})

def validateRatedBlunder(blunder_id, user_line, spent_time):
    # In rated mode, anonymous users have nothing to validate, this is correct situation
    if session.isAnonymous():
        return jsonify({'status': 'ok'})

    return jsonify(validate(blunder_id, user_line, spent_time, const.tasks.RATED))

def validatePackBlunder(blunder_id, user_line, spent_time):
    # In pack mode, anonimous user can't validate, this is error
    if session.isAnonymous():
        return jsonify({
            'status': 'error',
            'message': "Working with packs in anonymous mode is not supported"
        })

    return jsonify(validate(blunder_id, user_line, spent_time, const.tasks.PACK))

@app.route('/api/blunder/validate', methods = ['POST'])
def validateBlunder():
    try:
        blunder_id = request.json['id']
        user_line = request.json['line']
        spent_time = request.json['spentTime']
        type = request.json['type']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Blunder id, user line, spent time and type required'
        })

    if type == const.tasks.RATED:
        return validateRatedBlunder(blunder_id, user_line, spent_time)
    elif type == const.tasks.EXPLORE:
        return validateExploreBlunder(blunder_id, user_line, spent_time)
    elif type == const.tasks.PACK:
        return validatePackBlunder(blunder_id, user_line, spent_time)
    else:
        return jsonify({
            'status': 'error',
            'message': 'Blunder type must be explore,rated or pack'
        })

@app.route('/api/mobile/blunder/validate', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def validateBlunderMobile():
    return validateBlunder()
