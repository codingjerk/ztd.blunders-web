
from app import app
from app.utils import wrappers, session

@app.route('/api/session/logout', methods = ['POST'])
@wrappers.nullable()
def logoutWeb():
    session.deauthorize()
    return {
        'status': 'ok'
    }
