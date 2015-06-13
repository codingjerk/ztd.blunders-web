from flask import render_template, request, redirect

from app import app
from app.db import postgre
from app.utils import session

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', title = 'Ztd.Blunders', session = session)

@app.route('/login', methods=['POST'])
def login_post():
    session.authorize(request.form['username'], request.form['password'])
    return redirect('/')

@app.route('/logout')
def logout():
    session.deauthorize()
    return redirect('/')