from flask import jsonify

from app import app, db
from app.db import mongo, postgre
from app import utils
from app.utils import session

def assignNewBlunder():
    blunder = mongo.randomBlunder()
    postgre.assignBlunderTask(session.userID(), str(blunder['_id']))

    return blunder

@app.route('/getRandomBlunder', methods = ['POST'])
def getRandomBlunder():
    blunder = db.getAssignedBlunder(session.userID())

    if blunder is None:
        blunder = assignNewBlunder()

    data = utils.jsonifyBlunder(blunder)
    return jsonify(data)