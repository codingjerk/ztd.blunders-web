from flask import jsonify, request

import random

from app import app, db
from app.db import mongo, postgre
from app import utils

@app.route('/statistics/getBlundersStatistics', methods=['POST'])
def getBlundersStatistics():
    username = None
    try:
        username = request.json['username']
    except:
        pass

    if username is None:
        return jsonify(db.getBlundersStatistics())              # server statistics
    else:
        return jsonify(postgre.getBlundersStatistics(username)) # user statistics
    