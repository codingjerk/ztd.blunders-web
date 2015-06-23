from flask import jsonify, request

from app import app
from app.db import postgre

@app.route('/statistics/getBlundersByDate', methods=['POST'])
def getBlundersByDate():
    try:
        username = request.json['username']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Username required'
        })

    return jsonify(postgre.getBlundersByDate(username))
