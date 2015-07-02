from flask import jsonify

from app import app
from app.db import postgre

@app.route('/statistic/getUsersByRating', methods = ['GET'])
def getUsersByRating():
    return jsonify(postgre.getUsersByRating(50))
