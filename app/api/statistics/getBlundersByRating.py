from flask import jsonify

from app import app
from app.db import postgre

@app.route('/statistics/getBlundersByRating', methods = ['GET'])
def getBlundersByRating():
    return jsonify(postgre.getBlandersByRating(50))
