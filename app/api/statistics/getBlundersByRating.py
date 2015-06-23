from flask import jsonify

from app import app
from app.db import mongo

@app.route('/statistics/getBlundersByRating', methods = ['GET'])
def getBlundersByRating():
    return jsonify(mongo.getBlandersByRating(50))
