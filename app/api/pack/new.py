
from flask import request, jsonify

from app import app
from app.db import postgre
from app import utils
from app.utils import session, const, crossdomain

#TODO: What if duplicates in blunder Tasks?

def newRandomPack(pack_description):
    blunder_ids = [
        postgre.blunder.getRandomBlunder()['id']
        for index in range(25)
    ]

    pack_id = postgre.pack.createPack(session.userID(), blunder_ids, const.pack_type.RANDOM, {}, pack_description)
    postgre.pack.assignPack(session.userID(), pack_id)

    return pack_id

# Type name and tag name is different beasts, but this function handles
# the most simple case when they are the same.
# Request for pack type_name, which consists of blunders tagged by tag name equals to type_name
def newPackByTagName(pack_type_name, pack_description):
    blunder_ids = postgre.blunder.getBlunderByTag(pack_type_name, 25)

    pack_id = postgre.pack.createPack(session.userID(), blunder_ids, pack_type_name, {}, pack_description)
    postgre.pack.assignPack(session.userID(), pack_id)

    return pack_id

def newMateInNPack(pack_type_args, pack_description):
    try:
        N = pack_type_args['N']
    except Exception:
        return None

    tag_name = "Mate in %s" % (N,)
    blunder_ids = postgre.blunder.getBlunderByTag(tag_name, 25)

    pack_id = postgre.pack.createPack(session.userID(), blunder_ids, const.pack_type.MATEINN, pack_type_args, pack_description)
    postgre.pack.assignPack(session.userID(), pack_id)

    return pack_id

def newPackRatingAboutX(pack_type_args, pack_description):
    try:
        rating = pack_type_args['rating']
    except Exception:
        return None

    if rating <= 0:
        return None

    deviation = 50

    blunder_ids = postgre.blunder.getBlunderByRating(rating, deviation, 25)
    if len(blunder_ids) < 25:
        return None

    pack_id = postgre.pack.createPack(session.userID(), blunder_ids, const.pack_type.RATINGABOUTX, pack_type_args, pack_description)
    postgre.pack.assignPack(session.userID(), pack_id)

    return pack_id

# Some requests mean virtual pack requests, where parameters must
# Be calculated only during creation time, now.
# For most cases, will be just identity method
def transformPackRequest(pack_type_name, pack_type_args, pack_description):
    # USERLEVEL packs are simply RATINGABOUTX packs with rating taken from user current rating
    if pack_type_name == const.pack_type.USERLEVEL:
        rating = int(round(postgre.user.getRating(session.userID())/50)*50) # Round to closest xx50
        pack_type_name = const.pack_type.RATINGABOUTX
        pack_type_args = {
            'rating' : rating
        }
        pack_description = "Rating about %s" % rating

    return pack_type_name, pack_type_args, pack_description

def reusePack(pack_type_name, pack_type_args):
    pack_id = postgre.pack.reusePack(session.userID(), pack_type_name, pack_type_args)
    if(pack_id == None):
        return None

    postgre.pack.assignPack(session.userID(), pack_id)

    return pack_id

def packSelector(pack_type_name, pack_type_args):
    assigned_packs, unlocked_packs = postgre.pack.getPacks(session.userID())
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

    if len(filtered) > 1:
        return { # Duplicates in pack_type_name's in unlocked array are now allowed
            'status': 'error',
            'message': 'Internal error in algorithm of pack creation: %s' % pack_type_name
        }

    if len(filtered) != 1:
        return {
            'status': 'error',
            'message': 'Pack type name is not exist or locked for user: %s' % pack_type_name
        }

    # Setting new pack's description. Can be anything, changeable by user
    pack_description = filtered[0]['description']

    # If we need to transform some unlocked requests, do it here
    pack_type_name, pack_type_args, pack_description = transformPackRequest(pack_type_name, pack_type_args, pack_description)

    # Reuse pack mechanism. This keeps database from growing too much and
    # give better interaction experience between users
    pack_id = reusePack(pack_type_name, pack_type_args)
    if(pack_id != None):
        return {
            'status': 'ok',
            'data': {
                'pack_id': postgre.pack.idToHashId(pack_id)
            }
        }

    if pack_type_name == const.pack_type.RANDOM:
        pack_id = newRandomPack(pack_description)
    elif pack_type_name == const.pack_type.MATEINN:
        pack_id = newMateInNPack(pack_type_args, pack_description)
    elif pack_type_name == const.pack_type.GRANDMASTERS:
        pack_id = newPackByTagName(pack_type_name, pack_description)
    elif pack_type_name == const.pack_type.OPENING:
        pack_id = newPackByTagName(pack_type_name, pack_description)
    elif pack_type_name == const.pack_type.ENDGAME:
        pack_id = newPackByTagName(pack_type_name, pack_description)
    elif pack_type_name == const.pack_type.PROMOTION:
        pack_id = newPackByTagName(pack_type_name, pack_description)
    elif pack_type_name == const.pack_type.CLOSEDGAME:
        pack_id = newPackByTagName(pack_type_name, pack_description)
    elif pack_type_name == const.pack_type.RATINGABOUTX:
        pack_id = newPackRatingAboutX(pack_type_args, pack_description)
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
            'pack_id': postgre.pack.idToHashId(pack_id)
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
