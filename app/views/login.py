from flask import render_template

from app import app
from app.utils import session

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', title = 'Ztd.Blunders', session = session)
