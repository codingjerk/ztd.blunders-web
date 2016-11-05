from flask import jsonify, request

from app import app
from app.db import postgre
from app.utils import session, crossdomain

@app.route('/api/user/rating-by-date', methods=['POST'])
def getRatingByDate():
    try:
        username = request.json['username']
        interval = request.json['interval']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Username required'
        })

    return jsonify(postgre.user.getRatingByDate(username, mode))

@app.route('/api/mobile/user/rating-by-date', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def getRatingByDateMobile():
    # If 'username' not set, use default username associated with token.
    if not 'username' in request.json:
        request.json['username'] = session.username()

    return getRatingByDate()
