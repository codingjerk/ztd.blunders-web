from flask import request, jsonify

from app import app
from app.db import postgre
from app import utils
from app.utils import hash, session

@app.route('/api/session/signup', methods=['POST'])
def signup_post():
    username, password, email = (request.json[key] for key in ['username', 'password', 'email'])

    validateResult = utils.validateUser(username, password, email)
    if validateResult is not None:
        return jsonify(validateResult)

    salt, hashPass = hash.new(password)
    status = postgre.signupUser(username, salt, hashPass, email)

    if status['status'] == 'ok':
        session.authorize(username, password)

    return jsonify(status)