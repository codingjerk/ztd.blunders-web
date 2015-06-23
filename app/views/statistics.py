from flask import render_template, request

from app import app
from app.utils import session

@app.route('/statistics', methods=['GET'])
def statistics():
    username = request.args.get('user')
    if username is None:
        return render_template('statistics_server.html', title = 'Ztd.Blunders', session = session)

    return render_template('statistics_user.html', title = 'Ztd.Blunders', session = session)
