from flask import jsonify, request

import random

from app import app, db
from app.db import mongo, postgre
from app import utils

@app.route('/statistics/getUsersStatistics', methods=['GET'])
def getUsersStatistics():
    return jsonify(postgre.getUsersStatistics())
    