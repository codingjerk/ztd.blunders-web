from flask import request, jsonify

from app import app
from app.db import postgre
from app import utils
from app.utils import session, crossdomain

# This method removes pack from user's assinged packs
# Pack itself is not removed

@app.route('/api/pack/remove', methods = ['POST'])
def removePack():
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

    postgre.pack.removePack(session.userID(), pack_id, False)

    return jsonify({
        'status':'ok'
    })

@app.route('/api/mobile/pack/remove', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def removePackMobile():
    return removePack()
