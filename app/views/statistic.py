from flask import render_template, request

from app import app
from app.utils import session

@app.route('/statistic', methods=['GET'])
def statistic():
    username = request.args.get('user')
    if username is None:
        return render_template('server-statistic.html', title = 'Ztd.Blunders', session = session)

    return render_template('user-statistic.html', title = 'Ztd.Blunders', session = session)
