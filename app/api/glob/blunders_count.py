
from app import app
from app.db import postgre

from app.utils import wrappers, logger

logger = logger.Logger(__name__)

def totalBlundersCount():
    logger.info("API Handler global/blunders-count")

    return postgre.statistic.getBlundersStatistic()

@app.route('/api/global/blunders-count', methods=['POST'])
@wrappers.nullable()
def totalBlundersCountWeb():
    return totalBlundersCount()
