from flask import jsonify, request

from app import app
from app.db import postgre
from app.utils import session, crossdomain

@app.route('/api/user/blunders-by-date', methods=['POST'])
def getBlundersByDate():
    try:
        username = request.json['username']
        interval = request.json['interval']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Username required'
        })

    return jsonify(postgre.user.getBlundersByDate(username, mode))

@app.route('/api/mobile/user/blunders-by-date', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def getBlundersByDateMobile():
    # If 'username' not set, use default username associated with token.
    if not 'username' in request.json:
        request.json['username'] = session.username()

    return getBlundersByDate()
