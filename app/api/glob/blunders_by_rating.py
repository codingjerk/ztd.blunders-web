from flask import jsonify

from app import app
from app.db import postgre

@app.route('/api/global/blunders-by-rating', methods = ['POST'])
def getBlundersByRating():
    return jsonify(postgre.getBlandersByRating(50))
