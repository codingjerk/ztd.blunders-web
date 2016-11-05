from flask import jsonify, request

from app import app
from app.db import postgre
from app.utils import session, crossdomain

@app.route('/api/user/blunders-count', methods=['POST'])
def userBlundersCount():
    try:
        username = request.json['username']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Username required'
        })

    return jsonify(postgre.user.getBlundersStatistic(username))

@app.route('/api/mobile/user/blunders-count', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def userBlundersCountMobile():
    # If 'username' not set, use default username associated with token.
    if not 'username' in request.json:
        request.json['username'] = session.username()

    return userBlundersCount()
