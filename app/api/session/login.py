from flask import request, jsonify

from app import app
from app.utils import session

@app.route('/api/session/login', methods=['POST'])
def login_post():
    result = session.authorize(request.json['username'], request.json['password'])

    return jsonify(result)
