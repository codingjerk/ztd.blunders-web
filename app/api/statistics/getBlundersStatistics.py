from flask import jsonify, request

import random

from app import app, db
from app.db import mongo, postgre
from app import utils

@app.route('/statistics/getBlundersStatistics', methods=['POST'])
def getBlundersStatistics():
    try:
        username = request.json['username']
        return jsonify(postgre.getBlundersStatistics(username)) # user statistics
    except:
        return jsonify(db.getBlundersStatistics())              # server statistics
    