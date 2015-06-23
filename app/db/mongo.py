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

def randomBlunder():
    randomIndex = random.randrange(0, db['filtered_blunders'].count())

    return db['filtered_blunders'].find().skip(randomIndex).limit(1)[0]

def getBlunderById(blunder_id):
    requestResult = db['filtered_blunders'].find({'_id': ObjectId(blunder_id)})

    if requestResult.count() != 1:
        return None

    return requestResult[0]

def getGameById(game_id):
    requestResult = db['games'].find({'_id': ObjectId(game_id)})

    if requestResult.count() != 1:
        return None

    return requestResult[0]

def setRating(blunder_id, rating):
    db['filtered_blunders'].update({'_id': ObjectId(blunder_id)}, {'$set': {'elo': rating}})

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
