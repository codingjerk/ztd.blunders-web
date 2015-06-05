from app.db import mongo, postgre

from app.utils import elo

# TODO: Calculate real elo
def changeRating(user_id, blunder_id, success):
    if user_id is None: return

    blunder = mongo.getBlunderById(blunder_id)
    if blunder is None: return

    blunder_elo = blunder['elo']
    user_elo = postgre.getRating(user_id)

    newUserElo, newBlunderElo = elo.calculate(user_elo, blunder_elo, success)

    postgre.setRating(user_id, newUserElo)
    mongo.setRating(blunder_id, newBlunderElo)

    return newUserElo, (newUserElo - user_elo)

def getAssignedBlunder(user_id):
    if user_id is None: return None

    blunder_id = postgre.getAssignedBlunder(user_id)

    if blunder_id is None: return None

    return mongo.getBlunderById(blunder_id)