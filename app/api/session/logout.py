
from app import app
from app.utils import wrappers, session, logger

logger = logger.Logger(__name__)

@app.route('/api/session/logout', methods = ['POST'])
@wrappers.nullable()
def logoutWeb():
    logger.info("API Handler session/logout")

    session.deauthorize()
    return {
        'status': 'ok'
    }
