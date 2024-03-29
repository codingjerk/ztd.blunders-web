from flask import request

from app import app
from app.db import postgre
from app.utils import wrappers, session, const, chess, logger

from app.utils import elo, crossdomain

logger = logger.Logger(__name__)

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
    blunder = postgre.blunder.getBlunderById(blunder_id)
    if blunder is None:
        return {
            'status': 'error',
            'message': "Invalid blunder id"
        }

    date_start = postgre.blunder.getTaskStartDate(session.userID(), blunder_id, task_type)

    blunder_move = blunder['blunder_move']
    forced_line = blunder['forced_line']
    if chess.mismatchCheck(blunder_move, forced_line, user_line):
        return {
            'status': 'error',
            'message': "Remote database has been changed"
        }
    success = chess.compareLines(blunder_move, forced_line, user_line)

    if not postgre.blunder.closeBlunderTask(session.userID(), blunder_id, task_type):
        return {
            'status': 'error',
            'message': "Validation failed"
        }

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

    elo = blunder['elo']
    newElo, delta = changeRating(session.userID(), blunder_id, success)

    return {
        'data':{
            'elo': newElo,
            'delta': delta
            },
        'status': 'ok'
    }

def validateExploreBlunder(blunder_id, user_line, spent_time): #pylint: disable=unused-argument
    if session.isAnonymous():
        return {'status': 'ok'}

    # In explore mode, just remove blunder from task list
    # It is also ok, that there is no blunder to delete
    postgre.blunder.closeBlunderTask(session.userID(), blunder_id, const.tasks.EXPLORE)

    return {'status': 'ok'}

def validateRatedBlunder(blunder_id, user_line, spent_time):
    # In rated mode, anonymous users have nothing to validate, this is correct situation
    if session.isAnonymous():
        return {'status': 'ok'}

    return validate(blunder_id, user_line, spent_time, const.tasks.RATED)

def validatePackBlunder(blunder_id, user_line, spent_time):
    # In pack mode, anonymous user can't validate, this is error
    if session.isAnonymous():
        return {
            'status': 'error',
            'message': "Working with packs in anonymous mode is not supported"
        }

    result = validate(blunder_id, user_line, spent_time, const.tasks.PACK)

    # This is optional field, client should not rely on. Gets updated info of the position
    # so user can update it without need of sending separate info request
    result['data'].update({
        'info': postgre.blunder.getBlunderInfoById(session.userID(), blunder_id)
    })

    # Remove user asociated packs which are complatelly solved
    postgre.pack.gcHistoryPacks(session.userID())

    return result

def validateBlunder():
    logger.info("API Handler blunder/validate")

    try:
        blunder_id = request.json['id']
        user_line = request.json['line']
        spent_time = request.json['spentTime']
        type = request.json['type']
    except Exception:
        return {
            'status': 'error',
            'message': 'Blunder id, user line, spent time and type required'
        }

    if type == const.tasks.RATED:
        return validateRatedBlunder(blunder_id, user_line, spent_time)
    elif type == const.tasks.EXPLORE:
        return validateExploreBlunder(blunder_id, user_line, spent_time)
    elif type == const.tasks.PACK:
        return validatePackBlunder(blunder_id, user_line, spent_time)
    else:
        return {
            'status': 'error',
            'message': 'Blunder type must be explore,rated or pack'
        }

@app.route('/api/blunder/validate', methods = ['POST'])
@wrappers.nullable()
def validateBlunderWeb():
    return validateBlunder()

@app.route('/api/mobile/blunder/validate', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def validateBlunderMobile():
    return validateBlunder()
