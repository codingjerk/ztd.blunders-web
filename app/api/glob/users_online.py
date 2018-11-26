
from app import app
from app.db import postgre

from app.utils import wrappers, logger

logger = logger.Logger(__name__)

def getUsersOnline():
    logger.info("API Handler global/users-online")
    
    return {
        'status': 'ok',
        'data': {
            "users-online-list" : postgre.statistic.getActiveUsers('1 HOUR')
        }
    }

@app.route('/api/global/users-online', methods=['POST'])
@wrappers.nullable()
def getUsersOnlineWeb():
    return getUsersOnline()
