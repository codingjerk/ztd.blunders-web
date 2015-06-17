from flask import jsonify

from app import app, db
from app.db import mongo, postgre
from app import utils
from app.utils import session

def assignNewBlunder():
    blunder = mongo.randomBlunder()
    postgre.assignBlunderTask(session.userID(), str(blunder['_id']), 'rated')

    return blunder

@app.route('/getRatedBlunder', methods = ['POST'])
def getRatedBlunder():
    blunder = db.getAssignedBlunder(session.userID(), 'rated')

    if blunder is None:
        blunder = assignNewBlunder()

    data = utils.jsonifyBlunder(blunder)
    return jsonify(data)