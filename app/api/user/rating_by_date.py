from flask import jsonify, request

from app import app
from app.db import postgre

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
