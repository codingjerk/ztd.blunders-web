from flask import request, jsonify

from app import app
from app.db import postgre
from app.utils import session, crossdomain

from app.api.blunder.info import getBlunderInfoById

@app.route('/api/blunder/favorite', methods = ['POST'])
def favoriteBlunder():
    if session.isAnonymous():
        return jsonify({
            'status': 'error',
            'message': 'Favorites allowed only for authorized user'
        })

    try:
        blunder_id = request.json['blunder_id']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Blunder id required'
        })

    if not postgre.blunder.favoriteBlunder(session.userID(), blunder_id):
        return jsonify({
            'status': 'error',
            'message': "Can't favorite blunder"
        })

    return getBlunderInfoById(blunder_id)

@app.route('/api/mobile/blunder/favorite', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def favoriteBlunderMobile():
    return favoriteBlunder()
