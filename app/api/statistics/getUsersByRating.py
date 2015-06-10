from flask import jsonify, request

import random

from app import app, db
from app.db import mongo, postgre
from app import utils

@app.route('/statistics/getUsersByRating', methods = ['GET'])
def getUsersByRating():
    return jsonify(postgre.getUsersByRating(50))