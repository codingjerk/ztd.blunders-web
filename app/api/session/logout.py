from flask import jsonify

from app import app
from app.utils import session

@app.route('/api/session/logout', methods = ['POST'])
def logout():
    session.deauthorize()
    return jsonify({
        'status': 'ok'
    })
