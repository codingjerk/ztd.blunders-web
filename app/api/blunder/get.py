from flask import request, jsonify

from app import app
from app.db import postgre
from app import utils
from app.utils import session, const, crossdomain

def assignNewBlunder(taskType):
    blunder = postgre.blunder.getRandomBlunder()

    postgre.blunder.assignBlunderTask(session.userID(), str(blunder['id']), taskType)

    return blunder

def getRatedBlunder():
    blunder = postgre.blunder.getAssignedBlunder(session.userID(), const.tasks.RATED)

    if blunder is None:
        blunder = assignNewBlunder(const.tasks.RATED)

    data = utils.jsonifyBlunder(blunder)
    return jsonify(data)

def getExploreBlunder():
    blunder = postgre.blunder.getAssignedBlunder(session.userID(), const.tasks.EXPLORE)

    if 'id' in request.json:
        if blunder is not None:
            postgre.blunder.closeBlunderTask(session.userID(), request.json['id'], const.tasks.EXPLORE)

        blunder = postgre.blunder.getBlunderById(request.json['id'])
    else:
        if blunder is None:
            blunder = assignNewBlunder(const.tasks.EXPLORE)

    data = utils.jsonifyBlunder(blunder)
    return jsonify(data)

@app.route('/api/blunder/get', methods = ['POST'])
def getBlunder():
    try:
        type = request.json['type']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Blunder type required'
        })

    if type == 'rated':
        return getRatedBlunder()
    elif type == 'explore':
        return getExploreBlunder()
    else:
        return jsonify({
            'status': 'error',
            'message': 'Blunder type must be rated or explore'
        })

@app.route('/api/mobile/blunder/get', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def getBlunderMobile():
    return getBlunder()
