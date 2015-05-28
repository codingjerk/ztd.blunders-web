import random
import pymongo
from bson.objectid import ObjectId 

from app import utils

@utils.init
def main():
    global db

    mongo = pymongo.MongoClient('localhost', 27017)
    db = mongo['chessdb']

def randomBlunder():
    randomIndex = random.randrange(1, 2)#db['filtered_blunders'].count())

    return db['filtered_blunders'].find().skip(randomIndex).limit(1)[0]

def getBlunderById(blunder_id):
    requestResult = db['filtered_blunders'].find({'_id': ObjectId(blunder_id)})

    if requestResult.count() != 1: return None

    return requestResult[0]

def setRating(blunder_id, rating):
    db['filtered_blunders'].update({'_id': ObjectId(blunder_id)}, {'$set': {'elo': rating}})