from app.db import mongo, postgre

from app.utils import elo

# TODO: Calculate real elo
def changeRating(username, blunder_id, success):
    if username is None: return

    blunder = mongo.getBlunderById(blunder_id)
    if blunder is None: return

    blunder_elo = blunder['elo']
    user_elo = postgre.getRating(username)

    newUserElo, newBlunderElo = elo.calculate(user_elo, blunder_elo, success)

    postgre.setRating(username, newUserElo)
    mongo.setRating(blunder_id, newBlunderElo)

    return newUserElo, (newUserElo - user_elo)

def getAssignedBlunder(username):
    if username is None: return None

    blunder_id = postgre.getAssignedBlunder(username)

    if blunder_id is None: return None

    return mongo.getBlunderById(blunder_id)