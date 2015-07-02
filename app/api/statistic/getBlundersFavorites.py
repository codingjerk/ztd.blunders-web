from flask import jsonify, request

from app import app, db

@app.route('/statistic/getBlundersFavorites', methods = ['POST'])
def getBlundersFavorites():
    try:
        username = request.json['username']
        offset = request.json['offset']
        limit = request.json['limit']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Username, offset and limit required'
        })

    return jsonify(db.getBlundersFavorites(username, offset, limit))
