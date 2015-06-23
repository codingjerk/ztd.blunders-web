from flask import jsonify, request

from app import app
from app.db import postgre

@app.route('/statistics/getRatingByDate', methods=['POST'])
def getRatingByDate():
    try:
        username = request.json['username']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Username required'
        })

    return jsonify(postgre.getRatingByDate(username))
