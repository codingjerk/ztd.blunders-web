from flask import request

from app import app
from app.db import postgre
from app.utils import wrappers, session, crossdomain

def getBlundersByDate():
    try:
        username = request.json['username']
        interval = request.json['interval']
    except Exception:
        return {
            'status': 'error',
            'message': 'Username and interval required'
        }

    return postgre.user.getBlundersByDate(username, interval)

@app.route('/api/user/blunders-by-date', methods=['POST'])
@wrappers.nullable()
def getBlundersByDateWeb():
    return getBlundersByDate()

@app.route('/api/mobile/user/blunders-by-date', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def getBlundersByDateMobile():
    # If 'username' not set, use default username associated with token.
    if not 'username' in request.json:
        request.json['username'] = session.username()

    return getBlundersByDate()
