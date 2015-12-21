import pymongo
from datetime import datetime

from bson.objectid import ObjectId

from app import utils

db = None

@utils.init
def main():
    global db #pylint: disable=global-statement

    mongo = pymongo.MongoClient('localhost', 27017, connect = False)
    db = mongo['chessdb']

def getFromCache(type):
    requestResult = db['cache'].find({'type':type})

    if requestResult.count() == 0:
        return None

    return requestResult[0]['content']

def setInCache(type, data, expireTime):
    db['cache'].insert({'type':type, expireTime: datetime.utcnow(), 'content':data})
