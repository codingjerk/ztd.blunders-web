from datetime import datetime

from app.db import redis

def cached(type, expireTime):
    def decorator(func):
        def result(*args):
            cachedData = redis.getFromCache(type);
            if cachedData is None:
                calculatedData = func(*args);
                redis.setInCache(type, calculatedData, expireTime)
                return calculatedData

            return cachedData

        return result

    return decorator
