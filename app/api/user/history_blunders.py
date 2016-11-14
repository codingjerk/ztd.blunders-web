from flask import jsonify, request

from app import app
from app.db import postgre
from app.utils import session, crossdomain

@app.route('/api/user/history-blunders', methods = ['POST'])
def getBlundersHistory():
    try:
        username = request.json['username']
        offset = request.json['offset']
        limit = request.json['limit']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Username, offset and limit required'
        })

    return jsonify(postgre.statistic.getBlundersHistory(username, offset, limit))

@app.route('/api/mobile/user/history-blunders', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def getBlundersHistoryMobile():
    # If 'username' not set, use default username associated with token.
    if not 'username' in request.json:
        request.json['username'] = session.username()

    return getBlundersHistory()
