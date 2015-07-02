from flask import jsonify, request

from app import app, db

@app.route('/statistic/getCommentsByUser', methods = ['POST'])
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

    return jsonify(db.getCommentsByUser(username, offset, limit))
