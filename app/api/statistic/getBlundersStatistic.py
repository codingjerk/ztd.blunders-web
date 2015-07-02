from flask import jsonify, request

from app import app, db
from app.db import postgre

@app.route('/statistic/getBlundersStatistic', methods=['POST'])
def getBlundersStatistic():
    username = None
    try:
        username = request.json['username']
    except Exception:
        pass

    if username is None:
        return jsonify(db.getBlundersStatistic())              # server statistic
    else:
        return jsonify(postgre.getBlundersStatistic(username)) # user statistic
