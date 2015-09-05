from flask import jsonify

from app import app
from app.db import postgre

@app.route('/api/global/users-count', methods=['POST'])
def getUsersCount():
    return jsonify(postgre.getUsersCount())
