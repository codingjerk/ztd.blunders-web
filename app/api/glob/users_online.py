
from app import app
from app.db import postgre

from app.utils import wrappers

def getUsersOnline():
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
