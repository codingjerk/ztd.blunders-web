from flask import request, jsonify

from app import app
from app.db import postgre
from app import utils
from app.utils import session, tasks

def assignNewBlunder(taskType):
    blunder = postgre.getRandomBlunder()

    postgre.assignBlunderTask(session.userID(), str(blunder['id']), taskType)

    return blunder

def getRatedBlunder():
    blunder = postgre.getAssignedBlunder(session.userID(), tasks.RATED)

    if blunder is None:
        blunder = assignNewBlunder(tasks.RATED)

    data = utils.jsonifyBlunder(blunder)
    return jsonify(data)

def getExploreBlunder():
    blunder = postgre.getAssignedBlunder(session.userID(), tasks.EXPLORE)

    if 'id' in request.json:
        if blunder is not None:
            postgre.closeBlunderTask(session.userID(), request.json['id'], tasks.EXPLORE)

        blunder = postgre.getBlunderById(request.json['id'])
    else:
        if blunder is None:
            blunder = assignNewBlunder(tasks.EXPLORE)

    data = utils.jsonifyBlunder(blunder)
    return jsonify(data)

@app.route('/api/get-blunder', methods = ['POST'])
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