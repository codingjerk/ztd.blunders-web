from flask import render_template, request, redirect, session
from app import app

from app.db import postgre

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', title = 'Ztd.Blunders')

@app.route('/login', methods=['POST'])
def login_post():
    autentithicateSuccessful = postgre.autentithicateUser(request.form['username'], request.form['password'])

    if autentithicateSuccessful:
        session['username'] = request.form['username']
        return redirect('/')

    return redirect('/')

@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    
    return redirect('#')