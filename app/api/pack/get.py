from flask import request, jsonify

from app import app
from app.db import postgre
from app import utils
from app.utils import session, tasks, crossdomain

@app.route('/api/pack/get', methods = ['POST'])
def getPack():
    try:
        pack_id = request.json['pack_id']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Error in pack get'
        })

    if(session.isAnonymous()):
        return jsonify({
            'status': 'error',
            'message': 'Working with packs in anonymous mode is not supported'
        })

    blunder_ids = postgre.pack.getAssignedBlunders(session.userID(), pack_id)
    if blunder_ids is None:
        return jsonify({
            'status': 'error',
            'message': 'This pack not exists or not assigned to user'
        })

    blunders = [
        postgre.blunder.getBlunderById(blunder_id)
        for blunder_id in blunder_ids
    ]

    return jsonify({
        'status':'ok',
        'data': {
            'pack_id': pack_id,
            'blunders': blunders
        }
    })

@app.route('/api/mobile/pack/get', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def getPackMobile():
    return getPack()
