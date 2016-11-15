import base64

from datetime import datetime

from app.db import redis

def genKey(type, *args):
    joined =  "-".join([str(arg) for arg in args])
    encoded = base64.b64encode(str.encode(joined)).decode(encoding='utf-8')
    return "%s:%s" % (type, encoded)

def cached(type, expireTime):
    def decorator(func):
        def result(*args):
            key = genKey(type, *args)
            cachedData = redis.getFromCache(key);
            if cachedData is None:
                calculatedData = func(*args);
                redis.setInCache(key, calculatedData, expireTime)
                return calculatedData

            return cachedData

        return result

    return decorator
