from flask import jsonify, request

from app import app
from app.db import postgre

@app.route('/api/user/passed-blunders', methods = ['POST'])
def getBlundersHistory():
    try:
        username = request.json['username']
        offset = request.json['offset']
        limit = request.json['limit']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Username, offset and limit required'
        })

    return jsonify(postgre.user.getBlundersHistory(username, offset, limit))
