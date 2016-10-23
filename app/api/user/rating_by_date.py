from flask import jsonify, request

from app import app
from app.db import postgre
from app.utils import session, crossdomain

@app.route('/api/user/rating-by-date', methods=['POST'])
def getRatingByDate():
    try:
        username = request.json['username']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Username required'
        })

    return jsonify(postgre.user.getRatingByDate(username))

@app.route('/api/mobile/user/rating-by-date', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def getRatingByDateMobile():
    return getRatingByDate()
