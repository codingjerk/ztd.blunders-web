from flask import jsonify, request

import random

from app import app, db
from app.db import mongo, postgre
from app import utils

@app.route('/statistics/getBlundersByRating', methods = ['GET'])
def getBlundersByRating():
    return jsonify(mongo.getBlandersByRating(50))