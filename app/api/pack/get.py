from flask import request, jsonify

from app import app
from app.db import postgre
from app import utils
from app.utils import session, crossdomain

@app.route('/api/pack/get', methods = ['POST'])
def getPack():
    try:
        hash_id = request.json['pack_id']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Pack id required'
        })

    pack_id = postgre.pack.hashIdToId(hash_id)
    if(pack_id is None):
        return jsonify({
            'status': 'error',
            'message': 'Pack with given hash id not found'
        })

    if(session.isAnonymous()):
        return jsonify({
            'status': 'error',
            'message': 'Working with packs in anonymous mode is not supported'
        })

    pack_info = postgre.pack.getPackInfo(pack_id)
    if pack_info is None:
        return jsonify({
            'status': 'error',
            'message': 'This pack not exist'
        })
    caption = pack_info['caption']
    body = pack_info['body']

    blunder_ids = postgre.pack.getAssignedBlunders(session.userID(), pack_id)
    if blunder_ids is None:
        return jsonify({
            'status': 'error',
            'message': 'This pack not assigned to user'
        })

    blunders = [
        {
            'get': utils.jsonifyBlunder(postgre.blunder.getBlunderById(blunder_id)),
            'info': postgre.blunder.getBlunderInfoById(session.userID(), blunder_id)
        }
        for blunder_id in blunder_ids
    ]

    return jsonify({
        'status':'ok',
        'data': {
            'caption': caption,
            'body': body,
            'pack_id': postgre.pack.idToHashId(pack_id),
            'blunders': blunders
        }
    })

@app.route('/api/mobile/pack/get', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def getPackMobile():
    return getPack()
