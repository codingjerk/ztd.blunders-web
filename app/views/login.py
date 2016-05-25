from flask import render_template

from app import app
from app.utils import session,const

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', title = const.app.title, session = session)
