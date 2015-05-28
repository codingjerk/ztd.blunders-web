from flask import jsonify

from app import app, db
from app.db import mongo, postgre
from app import utils
from app.utils import session

def newBlunder():
    blunder = mongo.randomBlunder()
    postgre.assignBlunderTask(session.username(), str(blunder['_id']))
    return blunder

@app.route('/getRandomBlunder')
def getRandomBlunder():
    blunder = db.getAssignedBlunder(session.username())

    if blunder is None:
        blunder = newBlunder()

    data = utils.jsonifyBlunder(blunder)
    return jsonify(data)