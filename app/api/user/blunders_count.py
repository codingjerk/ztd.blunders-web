from flask import request

from app import app
from app.db import postgre
from app.utils import wrappers, session, crossdomain

def userBlundersCount():
    try:
        username = request.json['username']
    except Exception:
        return {
            'status': 'error',
            'message': 'Username required'
        }

    return postgre.user.getBlundersStatistic(username)

@app.route('/api/user/blunders-count', methods=['POST'])
@wrappers.nullable()
def userBlundersCountWeb():
    return userBlundersCount()

@app.route('/api/mobile/user/blunders-count', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def userBlundersCountMobile():
    # If 'username' not set, use default username associated with token.
    if not 'username' in request.json:
        request.json['username'] = session.username()

    return userBlundersCount()
