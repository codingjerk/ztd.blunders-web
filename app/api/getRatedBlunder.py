from flask import jsonify

from app import app, db
from app.db import mongo, postgre
from app import utils
from app.utils import session, tasks

def assignNewBlunder():
    blunder = mongo.randomBlunder()
    postgre.assignBlunderTask(session.userID(), str(blunder['_id']), tasks.RATED)

    return blunder

@app.route('/getRatedBlunder', methods = ['POST'])
def getRatedBlunder():
    blunder = db.getAssignedBlunder(session.userID(), tasks.RATED)

    if blunder is None:
        blunder = assignNewBlunder()

    data = utils.jsonifyBlunder(blunder)
    return jsonify(data)