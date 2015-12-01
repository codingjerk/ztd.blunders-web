from datetime import datetime

from app.db import mongo

def cached(type, expireTime):
    def decorator(func):
        def result(*args):
            cachedData = mongo.getFromCache(type);
            if cachedData is None:
                calculatedData = func(*args);
                mongo.setInCache(type, calculatedData, expireTime)
                return calculatedData

            return cachedData

        return result

    return decorator

