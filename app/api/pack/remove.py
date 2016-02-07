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
        pack_id = request.json['pack_id']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Pack id required'
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
