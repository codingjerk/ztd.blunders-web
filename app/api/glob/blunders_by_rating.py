
from app import app
from app.db import postgre

from app.utils import wrappers

def getBlundersByRating():
    return postgre.statistic.getBlundersByRating(50)

@app.route('/api/global/blunders-by-rating', methods = ['POST'])
@wrappers.nullable()
def getBlundersByRatingWeb():
    return getBlundersByRating()
