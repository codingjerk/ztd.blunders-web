
from flask import request

from app import app
from app.db import postgre
from app import utils
from app.utils import wrappers, session, const, crossdomain, logger

logger = logger.Logger(__name__)

#TODO: What if duplicates in blunder Tasks?

def sliderValidate(select_user, select_unlocked):
    # For slide, user's input must be anteger
    try:
        value = select_unlocked['min']
        while value <= select_unlocked['max']:
            if value == select_user:
                return True
            value = value + select_unlocked['step']

        return False
    except Exception: # What if user passed a string
        return False

def validateSelects(pack_type_args_user, pack_type_args_unlocked):
    for select_name in pack_type_args_unlocked:
        if not select_name in pack_type_args_user:
            return False

        select_type = pack_type_args_unlocked[select_name]['type']
        if select_type == 'slider':
            if not sliderValidate(pack_type_args_user[select_name],
                                  pack_type_args_unlocked[select_name]): return False
        else:
            return False # Unknown select type

    return True

def createPack(blunder_ids, pack_type_name, pack_type_args, pack_caption, pack_body):
    pack_id = postgre.pack.createPack(session.userID(), blunder_ids, pack_type_name, pack_type_args, pack_caption, pack_body)
    postgre.pack.assignPack(session.userID(), pack_id)

    return pack_id

def newRandomPack(pack_caption, pack_body):
    blunder_ids = [
        postgre.blunder.getRandomBlunder()['id']
        for index in range(const.pack.DEFAULT_SIZE)
    ]

    return createPack(blunder_ids, const.pack_type.RANDOM, {}, pack_caption, pack_body)

# Type name and tag name is different beasts, but this function handles
# the most simple case when they are the same.
# Request for pack type_name, which consists of blunders tagged by tag name equals to type_name
def newPackByTagName(pack_type_name, pack_caption, pack_body):
    blunder_ids = postgre.blunder.getBlunderByTag(pack_type_name, const.pack.DEFAULT_SIZE)

    return createPack(blunder_ids, pack_type_name, {}, pack_caption, pack_body)

def newMateInNPack(pack_type_args, pack_caption, pack_body):
    try:
        N = pack_type_args['N']
    except Exception:
        return None

    tag_name = "Mate in %s" % (N,)
    blunder_ids = postgre.blunder.getBlunderByTag(tag_name, const.pack.DEFAULT_SIZE)

    pack_caption = "Mate in %s" % (N,) # override default caption

    return createPack(blunder_ids, const.pack_type.MATEINN, pack_type_args, pack_caption, pack_body)

def newPackDifficultyLevels(pack_type_args, pack_caption, pack_body):
    try:
        rating = pack_type_args['rating']
    except Exception:
        return None

    if rating <= 0:
        return None

    deviation = 50

    blunder_ids = postgre.blunder.getBlunderByRating(rating, deviation, const.pack.DEFAULT_SIZE)
    if len(blunder_ids) < const.pack.DEFAULT_SIZE:
        return None

    pack_caption = 'Difficulty: %s' % rating # override default caption

    return createPack(blunder_ids, const.pack_type.DIFFICULTYLEVELS, pack_type_args, pack_caption, pack_body)

def newPackReplayFailed(pack_type_args, pack_caption, pack_body):
    blunder_ids = postgre.blunder.getBlunderForReplayFailed(session.userID(), const.pack.DEFAULT_SIZE)

    return createPack(blunder_ids, const.pack_type.REPLAYFAILED, {}, pack_caption, pack_body)

def reusePack(pack_type_name, pack_type_args):
    pack_id = postgre.pack.reusePack(session.userID(), pack_type_name, pack_type_args)
    if(pack_id == None):
        return None

    postgre.pack.assignPack(session.userID(), pack_id)

    return pack_id

def packSelector(pack_type_name, pack_type_args_user):
    assigned_packs, unlocked_packs = postgre.pack.getPacks(session.userID())

    pack_type_unlocked = [
        pack
        for pack in unlocked_packs
        if pack['type_name'] == pack_type_name
    ]

    if len(pack_type_unlocked) > 1:
        return { # Duplicates in pack_type_name's in unlocked array are not allowed
            'status': 'error',
            'message': 'Internal error in algorithm of pack creation: %s' % pack_type_name
        }

    if len(pack_type_unlocked) != 1:
        return {
            'status': 'error',
            'message': 'Pack type name is not exist or locked for user: %s' % pack_type_name
        }

    pack_type_args_unlocked = pack_type_unlocked[0]['args'] if 'args' in pack_type_unlocked[0] else {}

    if not validateSelects(pack_type_args_user, pack_type_args_unlocked):
        return { # User's input is illegal
            'status': 'error',
            'message': 'Illegal input received from user: %s' % pack_type_name
        }

    # Setting new pack's description. Can be anything, changeable by user
    # Currently, we create empty body for pack, reserving it for future use.
    # For example, user might want to edit pack body
    pack_caption = pack_type_unlocked[0]['caption']
    pack_body = '' #pack_type_unlocked[0]['body']

    # Reuse pack mechanism. This keeps database from growing too much and
    # give better interaction experience between users
    pack_id = reusePack(pack_type_name, pack_type_args_user)
    if(pack_id != None):
        return {
            'status': 'ok',
            'data': {
                'pack_id': postgre.pack.idToHashId(pack_id)
            }
        }

    if pack_type_name == const.pack_type.RANDOM:
        pack_id = newRandomPack(pack_caption, pack_body)
    elif pack_type_name == const.pack_type.MATEINN:
        pack_id = newMateInNPack(pack_type_args_user, pack_caption, pack_body)
    elif pack_type_name == const.pack_type.GRANDMASTERS:
        pack_id = newPackByTagName(pack_type_name, pack_caption, pack_body)
    elif pack_type_name == const.pack_type.OPENING:
        pack_id = newPackByTagName(pack_type_name, pack_caption, pack_body)
    elif pack_type_name == const.pack_type.ENDGAME:
        pack_id = newPackByTagName(pack_type_name, pack_caption, pack_body)
    elif pack_type_name == const.pack_type.PROMOTION:
        pack_id = newPackByTagName(pack_type_name, pack_caption, pack_body)
    elif pack_type_name == const.pack_type.CLOSEDGAME:
        pack_id = newPackByTagName(pack_type_name, pack_caption, pack_body)
    elif pack_type_name == const.pack_type.DIFFICULTYLEVELS:
        pack_id = newPackDifficultyLevels(pack_type_args_user, pack_caption, pack_body)
    elif pack_type_name == const.pack_type.REPLAYFAILED:
        pack_id = newPackReplayFailed(pack_type_args_user, pack_caption, pack_body)
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

def getNewPack():
    logger.info("API Handler pack/new")

    try:
        pack_type_name = request.json['type_name']
        pack_type_args_user = request.json['args'] if 'args' in request.json else {}
    except Exception:
        return {
            'status': 'error',
            'message': 'Type name required for pack type'
        }

    if(session.isAnonymous()):
        return {
            'status': 'error',
            'message': 'Working with packs in anonymous mode is not supported'
        }

    return packSelector(pack_type_name, pack_type_args_user)

@app.route('/api/pack/new', methods = ['POST'])
@wrappers.nullable()
def getNewPackWeb():
    return getNewPack()

@app.route('/api/mobile/pack/new', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def getNewPackMobile():
    return getNewPack()
