import pymongo

from bson.objectid import ObjectId

from app import utils

db = None

@utils.init
def main():
    global db #pylint: disable=global-statement

    mongo = pymongo.MongoClient('localhost', 27017)
    db = mongo['chessdb']


def getGameById(game_id):
    requestResult = db['games'].find({'_id': ObjectId(game_id)})

    if requestResult.count() != 1:
        return None

    return requestResult[0]
