from flask import jsonify, request

from app import app, db
from app.db import postgre

@app.route('/statistics/getBlundersStatistics', methods=['POST'])
def getBlundersStatistics():
    username = None
    try:
        username = request.json['username']
    except Exception:
        pass

    if username is None:
        return jsonify(db.getBlundersStatistics())              # server statistics
    else:
        return jsonify(postgre.getBlundersStatistics(username)) # user statistics
