from flask import request, jsonify

from app import app
from app.utils import session, crossdomain

@app.route('/api/session/login', methods=['POST'])
@session.nullable()
def login_post():
    try:
        username = request.json['username']
        password = request.json['password']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Username and password is required'
        })

    result = session.authorize(username, password)

    return jsonify(result)

@app.route('/api/mobile/session/login', methods=['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.nullable()
def login_post_mobile():
    try:
        username = request.json['username']
        password = request.json['password']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Username and password is required'
        })

    result = session.authorizeWithToken(username, password)

    return jsonify(result)
