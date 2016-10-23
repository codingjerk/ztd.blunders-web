from flask import jsonify, request

from app import app
from app.db import postgre
from app.utils import session, crossdomain

@app.route('/api/user/favorite-blunders', methods = ['POST'])
def getBlundersFavorites():
    try:
        username = request.json['username']
        offset = request.json['offset']
        limit = request.json['limit']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Username, offset and limit required'
        })

    return jsonify(postgre.statistic.getBlundersFavorites(username, offset, limit))

@app.route('/api/mobile/user/favorite-blunders', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def getBlundersFavoritesMobile():
    return getBlundersFavorites()
