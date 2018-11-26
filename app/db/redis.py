import redis
import json
from datetime import datetime

from app import utils
from app.utils import const

@utils.init
def main():
    global db #pylint: disable=global-statement

    pool = redis.ConnectionPool(
        host=const.redis.host,
        port=const.redis.port,
        db=const.redis.db
    )
    db = redis.Redis(connection_pool=pool)

def getFromCache(type):
    if not db.exists(type):
        return None

    return json.loads(db.get(type).decode("utf-8"))

def setInCache(type, data, expireTime):
    db.setex(
        name = type,
        value = json.dumps(data),
        time = expireTime
    )
