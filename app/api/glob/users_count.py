
from app import app
from app.db import postgre

from app.utils import wrappers, logger

logger = logger.Logger(__name__)

def getUsersCount():
    logger.info("API Handler global/users-count")

    return postgre.statistic.getUsersCount()

@app.route('/api/global/users-count', methods=['POST'])
@wrappers.nullable()
def getUsersCountWeb():
    return getUsersCount()
