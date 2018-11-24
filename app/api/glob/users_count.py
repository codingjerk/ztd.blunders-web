
from app import app
from app.db import postgre

from app.utils import wrappers

def getUsersCount():
    return postgre.statistic.getUsersCount()

@app.route('/api/global/users-count', methods=['POST'])
@wrappers.nullable()
def getUsersCountWeb():
    return getUsersCount()
