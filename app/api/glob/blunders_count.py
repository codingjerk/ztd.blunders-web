
from app import app
from app.db import postgre

from app.utils import wrappers

def totalBlundersCount():
    return postgre.statistic.getBlundersStatistic()

@app.route('/api/global/blunders-count', methods=['POST'])
@wrappers.nullable()
def totalBlundersCountWeb():
    return totalBlundersCount()
