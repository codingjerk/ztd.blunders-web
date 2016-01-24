
from flask import request, jsonify

from app import app
from app.db import postgre
from app import utils
from app.utils import session, const, crossdomain

#TODO: What if duplicates in blunder tasks?

def newRandomPack(pack_description):
    blunder_ids = [
        postgre.blunder.getRandomBlunder()['id']
        for index in range(25)
    ]

    pack_id = postgre.pack.createPack(session.userID(), blunder_ids, const.pack_type.RANDOM, {}, pack_description)
    postgre.pack.assignPack(session.userID(), pack_id)

    return pack_id

def newMateInNPack(pack_type_args, pack_description):
    try:
        N = pack_type_args['N']
    except Exception:
        return None

    blunder_ids = postgre.blunder.getMateTagBlunder(N, 25)

    pack_id = postgre.pack.createPack(session.userID(), blunder_ids, const.pack_type.MATEINN, pack_type_args, pack_description)
    postgre.pack.assignPack(session.userID(), pack_id)

    return pack_id

def packSelector(pack_type_name, pack_type_args):
    unlocked_packs = postgre.pack.getUnlockedPacks(session.userID())
    unlocked_keys = [(
                        pack['type_name'],
                        pack['args'] if 'args' in pack else {}
                      )
                    for pack in unlocked_packs]

    filtered = [
                pack
                for pack in unlocked_packs
                    if  (
                            pack['type_name'],
                            pack['args'] if 'args' in pack else {}
                        ) ==
                        (
                            pack_type_name,
                            pack_type_args
                        )
                ]
    if len(filtered) != 1:
        return {
            'status': 'error',
            'message': 'Pack type name is not exist or locked for user: %s' % pack_type_name
        }

    pack = filtered[0]
    # Setting new pack's description. Can be anything, changeable by user
    pack_description = pack['description']

    if pack_type_name == const.pack_type.RANDOM:
        pack_id = newRandomPack(pack_description)
    elif pack_type_name == const.pack_type.MATEINN:
        pack_id = newMateInNPack(pack_type_args, pack_description)
    else:
        return {
            'status': 'error',
            'message': 'Pack type name not supported: %s' % pack_type_name
        }

    if pack_id is None:
        return {
            'status': 'error',
            'message': 'Internal error in algorithm of pack creation: %s' % pack_type_name
        }

    return {
        'status': 'ok',
        'data': {
            'pack_id': pack_id
        }
    }

    # parse args

@app.route('/api/pack/new', methods = ['POST'])
def getNewPack():
    try:
        pack_type_name = request.json['type_name']
        pack_type_args = request.json['args'] if 'args' in request.json else {}
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

    return jsonify(packSelector(pack_type_name, pack_type_args))

@app.route('/api/mobile/pack/new', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def getNewPackMobile():
    return getNewPack()
