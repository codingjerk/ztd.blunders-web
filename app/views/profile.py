from flask import render_template, request

from app import app
from app.utils import session,const

@app.route('/profile', methods=['GET'])
def profile():
    userGet = request.args.get('user')
    username = userGet if userGet is not None else ''

    return render_template(
        'profile.html',
        title = const.app.title,
        session = session,
        username = username
    )
