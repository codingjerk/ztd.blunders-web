from flask import jsonify, request

import random

from app import app, db
from app.db import mongo, postgre
from app import utils

@app.route('/statistics/getBlundersStatistics', methods=['GET'])
def getBlundersStatistics():
    return jsonify(db.getBlundersStatistics())
    