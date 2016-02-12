from flask import request, jsonify

from app import app
from app.db import postgre
from app import utils
from app.utils import session, crossdomain

@app.route('/api/pack/info', methods = ['POST'])
def getPackInfo():
    try:
        pass
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Unknown'
        })

    if(session.isAnonymous()):
        return jsonify({
            'status': 'error',
            'message': 'Working with packs in anonymous mode is not supported'
        })

    packs, unlocked = postgre.pack.getPacks(session.userID())

    return jsonify({
        'status':'ok',
        'data': {
            'packs': packs,
            'unlocked': unlocked
        }
    })

@app.route('/api/mobile/pack/info', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def getPackInfoMobile():
    return getPackInfo()
