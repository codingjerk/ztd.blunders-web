
from flask import request, jsonify

from app import app
from app.db import postgre
from app import utils
from app.utils import session, const, crossdomain

#TODO: What if duplicates in blunder tasks?

def newRandomPack():
    blunder_ids = [
        postgre.blunder.getRandomBlunder()['id']
        for index in range(25)
    ]

    pack_id = postgre.pack.createPack(session.userID(), blunder_ids, const.pack_type.RANDOM)
    postgre.pack.assignPack(session.userID(), pack_id)

    return {
        'status': 'ok',
        'data': {
            'pack_id': pack_id
        }
    }

def packSelector(pack_type_name):
    unlocked_keys = [pack['type_name'] for pack in postgre.pack.getUnlockedPacks(session.userID())]
    if not (pack_type_name in unlocked_keys):
        return {
            'status': 'error',
            'message': 'Pack type name is not exist or locked for user: %s' % pack_type_name
        }

    if(pack_type_name == const.pack_type.RANDOM):
        return newRandomPack()
    else:
        return {
            'status': 'error',
            'message': 'Pack type name not supported: %s' % pack_type_name
        }

    # parse args

@app.route('/api/pack/new', methods = ['POST'])
def getNewPack():
    try:
        pack_type_name = request.json['type']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Type name required for pack type'
        })

    print (request.json)

    if(session.isAnonymous()):
        return jsonify({
            'status': 'error',
            'message': 'Working with packs in anonymous mode is not supported'
        })

    return jsonify(packSelector(pack_type_name))

@app.route('/api/mobile/pack/new', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def getNewPackMobile():
    return getNewPack()
