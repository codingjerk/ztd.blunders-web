from flask import render_template, request, redirect

from app import app
from app.db import postgre
from app.utils import session

@app.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html', title = 'Ztd.Blunders', session = session)
