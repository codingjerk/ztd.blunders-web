from flask import jsonify

from app import app, db

@app.route('/api/global/blunders-count', methods=['POST'])
def totalBlundersCount():
    return jsonify(db.getBlundersStatistic())
