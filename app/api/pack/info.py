from flask import request

from app import app
from app.db import postgre
from app import utils
from app.utils import wrappers, session, crossdomain

def getPackInfo():
    try:
        pass
    except Exception:
        return {
            'status': 'error',
            'message': 'Unknown'
        }

    if(session.isAnonymous()):
        return {
            'status': 'error',
            'message': 'Working with packs in anonymous mode is not supported'
        }

    packs, unlocked = postgre.pack.getPacks(session.userID())
    packs = [ postgre.pack.idToHashId(pack_id) for pack_id in packs]

    return {
        'status':'ok',
        'data': {
            'packs': packs,
            'unlocked': unlocked
        }
    }

@app.route('/api/pack/info', methods = ['POST'])
@wrappers.nullable()
def getPackInfoWeb():
    return getPackInfo()

@app.route('/api/mobile/pack/info', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def getPackInfoMobile():
    return getPackInfo()
