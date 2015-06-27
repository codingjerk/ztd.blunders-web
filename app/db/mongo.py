import random
import pymongo

from datetime import timedelta
from bson.objectid import ObjectId

from app import utils
from app.utils import cache

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

@cache.cached(timedelta(days = 1))
def getBlandersByRating(interval):
    result = db['filtered_blunders'].aggregate([
        {'$project':{'elo':'$elo','mod':{'$mod':['$elo', interval]}}},
        {'$project':{'elo_category': {'$subtract':['$elo','$mod']}}},
        {'$group':{'_id':{'elo_category':'$elo_category'},'count': {'$sum': 1}}}
    ])

    destribution = [[category['_id']['elo_category'], category['count']] for category in result]
    return {
        'status': 'ok',
        'data': {
            'blunders-rating-destribution' : destribution
        }
    }

def countBlunders():
    totalBlunders = db['filtered_blunders'].count()

    return totalBlunders
