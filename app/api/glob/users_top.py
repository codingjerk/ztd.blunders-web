
from app import app
from app.db import postgre

from app.utils import wrappers, logger

logger = logger.Logger(__name__)

def getUsersTop():
    logger.info("API Handler global/users-top")

    return {
        'status': 'ok',
        'data': {
            "users-top-by-rating": postgre.statistic.getUsersTopByRating(10),
            "users-top-by-activity": postgre.statistic.getUsersTopByActivity('1 WEEK', 10),
        }
    }


@app.route('/api/global/users-top', methods=['POST'])
@wrappers.nullable()
def getUsersTopWeb():
    return getUsersTop()
