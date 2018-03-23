from flask import request, jsonify

from app import app
from app.db import postgre
from app import utils
from app.utils import hash, session, crossdomain

@app.route('/api/session/signup', methods=['POST'])
def signup_post():
    return jsonify({
        'status': 'error',
        'message': 'New users are temporary disabled due to spammers'
    })

    username, password, email = (request.json[key] for key in ['username', 'password', 'email'])

    validateResult = utils.validateUser(username, password, email)
    if validateResult is not None:
        return jsonify(validateResult)

    salt, hashPass = hash.new(password)
    status = postgre.user.signupUser(username, salt, hashPass, email)

    if status['status'] == 'ok':
        session.authorize(username, password)

    return jsonify(status)

@app.route('/api/mobile/session/signup', methods=['POST', 'OPTIONS'])
@crossdomain.crossdomain()
def signup_post_mobile():
    return jsonify({
        'status': 'error',
        'message': 'New users are temporary disabled due to spammers'
    })

    try:
        username, password, email = (request.json[key] for key in ['username', 'password', 'email'])
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Username, password and email is required'
        })

    validateResult = utils.validateUser(username, password, email)
    if validateResult is not None:
        return jsonify(validateResult)

    salt, hashPass = hash.new(password)
    status = postgre.user.signupUser(username, salt, hashPass, email)

    if status['status'] != 'ok':
        return jsonify(status)

    return jsonify(
        session.authorizeWithToken(username, password)
    )
