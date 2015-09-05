from flask import render_template

from app import app
from app.utils import session

@app.route('/signup', methods=['GET'])
def signup_get():
    return render_template('signup.html', title = 'Ztd.Blunders', session = session)
