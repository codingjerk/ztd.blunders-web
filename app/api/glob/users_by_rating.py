
from app import app
from app.db import postgre

from app.utils import wrappers, logger

logger = logger.Logger(__name__)

def getUsersByRating():
    logger.info("API Handler global/users-by-rating")

    return postgre.statistic.getUsersByRating(50)

@app.route('/api/global/users-by-rating', methods = ['POST'])
@wrappers.nullable()
def getUsersByRatingWeb():
    return getUsersByRating()
