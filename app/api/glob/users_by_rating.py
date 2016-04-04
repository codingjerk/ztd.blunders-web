from flask import jsonify

from app import app
from app.db import postgre

@app.route('/api/global/users-by-rating', methods = ['POST'])
def getUsersByRating():
    return jsonify(postgre.statistic.getUsersByRating(50))
