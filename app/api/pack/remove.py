from flask import request

from app import app
from app.db import postgre
from app import utils
from app.utils import wrappers, session, crossdomain

# This method removes pack from user's assinged packs
# Pack itself is not removed

def removePack():
    try:
        hash_id = request.json['pack_id']
    except Exception:
        return {
            'status': 'error',
            'message': 'Pack id required'
        }

    pack_id = postgre.pack.hashIdToId(hash_id)
    if(pack_id is None):
        return {
            'status': 'error',
            'message': 'Pack with given hash id not found'
        }

    if(session.isAnonymous()):
        return {
            'status': 'error',
            'message': 'Working with packs in anonymous mode is not supported'
        }

    postgre.pack.removePack(session.userID(), pack_id, False)

    return {
        'status':'ok'
    }

@app.route('/api/pack/remove', methods = ['POST'])
@wrappers.nullable()
def removePackWeb():
    return removePack()

@app.route('/api/mobile/pack/remove', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def removePackMobile():
    return removePack()
