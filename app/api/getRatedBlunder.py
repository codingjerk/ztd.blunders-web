from flask import jsonify

from app import app, db
from app.db import mongo, postgre
from app import utils
from app.utils import session, TaskTypes

def assignNewBlunder():
    blunder = mongo.randomBlunder()
    postgre.assignBlunderTask(session.userID(), str(blunder['_id']), TaskTypes.RATED)

    return blunder

@app.route('/getRatedBlunder', methods = ['POST'])
def getRatedBlunder():
    blunder = db.getAssignedBlunder(session.userID(), TaskTypes.RATED)

    if blunder is None:
        blunder = assignNewBlunder()

    data = utils.jsonifyBlunder(blunder)
    return jsonify(data)