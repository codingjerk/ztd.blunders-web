from flask import request

from app import app
from app.db import postgre
from app import utils
from app.utils import wrappers, session, const, crossdomain, logger

logger = logger.Logger(__name__)

def assignNewBlunder(taskType):
    blunder = postgre.blunder.getRandomBlunder()

    postgre.blunder.assignBlunderTask(session.userID(), str(blunder['id']), taskType)

    return blunder

def getRatedBlunder():
    blunder = postgre.blunder.getAssignedBlunder(session.userID(), const.tasks.RATED)

    if blunder is None:
        blunder = assignNewBlunder(const.tasks.RATED)

    return {
        'status': 'ok',
        'data': utils.jsonifyBlunder(blunder)
    }

def getExploreBlunder():
    blunder = postgre.blunder.getAssignedBlunder(session.userID(), const.tasks.EXPLORE)

    if 'id' in request.json:
        if blunder is not None:
            postgre.blunder.closeBlunderTask(session.userID(), request.json['id'], const.tasks.EXPLORE)

        blunder = postgre.blunder.getBlunderById(request.json['id'])
    else:
        if blunder is None:
            blunder = assignNewBlunder(const.tasks.EXPLORE)

    return {
        'status': 'ok',
        'data': utils.jsonifyBlunder(blunder)
    }

def getBlunder():
    logger.info("API Handler blunder/get")

    try:
        type = request.json['type']
    except Exception:
        return {
            'status': 'error',
            'message': 'Blunder type required'
        }

    if type == 'rated':
        return getRatedBlunder()
    elif type == 'explore':
        return getExploreBlunder()
    else:
        return {
            'status': 'error',
            'message': 'Blunder type must be rated or explore'
        }

@app.route('/api/blunder/get', methods = ['POST'])
@wrappers.nullable()
def getBlunderWeb():
    return getBlunder()

@app.route('/api/mobile/blunder/get', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def getBlunderMobile():
    return getBlunder()
