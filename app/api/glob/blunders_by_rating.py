
from app import app
from app.db import postgre

from app.utils import wrappers, logger

logger = logger.Logger(__name__)

def getBlundersByRating():
    logger.info("API Handler global/blunders-by-rating")

    return postgre.statistic.getBlundersByRating(50)

@app.route('/api/global/blunders-by-rating', methods = ['POST'])
@wrappers.nullable()
def getBlundersByRatingWeb():
    return getBlundersByRating()
