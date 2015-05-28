from app.db import mongo, postgre

# TODO: Calculate real elo
def changeRating(username, blunder_id, success):
    if username is None: return

    blunder = mongo.getBlunderById(blunder_id)
    if blunder is None: return

    blunder_elo = blunder['elo']
    user_elo = postgre.getRating(username)

    delta = 11 if success else -11

    newUserElo = user_elo + delta
    newBlunderElo = blunder_elo - delta

    postgre.setRating(username, newUserElo)
    mongo.setRating(blunder_id, newBlunderElo)

    return newUserElo, delta

def getAssignedBlunder(username):
    if username is None: return None

    blunder_id = postgre.getAssignedBlunder(username)

    if blunder_id is None: return None

    return mongo.getBlunderById(blunder_id)