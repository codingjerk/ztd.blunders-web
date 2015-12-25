from flask import jsonify, request

from app import app
from app.db import postgre

@app.route('/api/user/comments', methods = ['POST'])
def getCommentsByUser():
    try:
        username = request.json['username']
        offset = request.json['offset']
        limit = request.json['limit']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Username, offset and limit required'
        })

    return jsonify(postgre.statistic.getCommentsByUser(username, offset, limit))
