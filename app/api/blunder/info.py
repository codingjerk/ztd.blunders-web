from flask import request

from app import app
from app.db import postgre
from app.utils import wrappers, session, crossdomain

def getBlunderInfo():
    try:
        blunder_id = request.json['blunder_id']
    except Exception:
        return {
            'status': 'error',
            'message': 'Blunder id required'
        }

    result = postgre.blunder.getBlunderInfoById(session.userID(), blunder_id)
    if result is None:
        return {
            'status': 'error',
            'message': 'Invalid blunder id',
        }

    return {
        'status': 'ok',
        'data': result
    }

@app.route('/api/blunder/info', methods=['POST'])
@wrappers.nullable()
def getBlunderInfoWeb():
    return getBlunderInfo()

@app.route('/api/mobile/blunder/info', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def getBlunderInfoMobile():
    return getBlunderInfo()
