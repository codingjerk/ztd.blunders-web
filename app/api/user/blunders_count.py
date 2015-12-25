from flask import jsonify, request

from app import app
from app.db import postgre

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

