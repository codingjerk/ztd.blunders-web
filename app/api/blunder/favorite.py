from flask import request

from app import app
from app.db import postgre
from app.utils import wrappers, session, crossdomain

def favoriteBlunder():
    if session.isAnonymous():
        return {
            'status': 'error',
            'message': 'Favorites allowed only for authorized user'
        }

    try:
        blunder_id = request.json['blunder_id']
    except Exception:
        return {
            'status': 'error',
            'message': 'Blunder id required'
        }

    if not postgre.blunder.favoriteBlunder(session.userID(), blunder_id):
        return {
            'status': 'error',
            'message': "Can't favorite blunder"
        }

    result = postgre.blunder.getBlunderInfoById(session.userID(), blunder_id)
    if result is None:
        return {
            'status': 'error',
            'message': 'Invalid blunder id',
        }

    return {
        'status': 'ok',
        'data': result
    }

@app.route('/api/blunder/favorite', methods = ['POST'])
@wrappers.nullable()
def favoriteBlunderWeb():
    return favoriteBlunder()

@app.route('/api/mobile/blunder/favorite', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def favoriteBlunderMobile():
    return favoriteBlunder()
