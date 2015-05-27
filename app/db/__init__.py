from bson.objectid import ObjectId 

from app.db import mongo, postgre

from app.utils import elo

# TODO: Calculate real elo
def changeRating(username, blunder_id, success):
    data = mongo.db['filtered_blunders'].find({'_id': ObjectId(blunder_id)})
    if data.count() != 1: return
    blunder = data[0]

    blunder_elo = blunder['elo']
    user_elo = postgre.getRating(username)

    newUserElo, newBlunderElo = elo.calculate(user_elo, blunder_elo, success)

    postgre.setRating(username, newUserElo)
    mongo.db['filtered_blunders'].update({'_id': ObjectId(blunder_id)}, {'$set': {'elo': newBlunderElo}})

    return newUserElo, (newUserElo - user_elo)

def getAssignedBlunder(username):
    if username is None: return None

    blunder_id = postgre.getAssignedBlunder(username)

    if blunder_id is None: return None

    data = mongo.db['filtered_blunders'].find({'_id': ObjectId(blunder_id)})

    if data.count() != 1: return None

    return data[0]