from flask import jsonify, request

from app import app
from app.db import postgre
from app.utils import session, crossdomain

@app.route('/api/blunder/info', methods=['POST'])
@crossdomain.crossdomain()
def getBlunderInfo():
    try:
        blunder_id = request.json['blunder_id']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Blunder id required'
        })

    result = postgre.blunder.getBlunderInfoById(session.userID(), blunder_id)
    if result is None:
        return {
            'status': 'error',
            'message': 'Invalid blunder id',
        }

    return jsonify({
        'status': 'ok',
        'data': result
    })

@app.route('/api/mobile/blunder/info', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def getBlunderInfoMobile():
    return getBlunderInfo()
