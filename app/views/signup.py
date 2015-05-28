from flask import render_template, request, redirect, session, jsonify
from app import app

from app.db import postgre

@app.route('/signup', methods=['GET'])
def signup_get():
    return render_template('signup.html', title = 'Ztd.Blunders')

@app.route('/signup', methods=['POST'])
def signup_post():
    username, password, email = request.json['username'], request.json['password'], request.json['email']

    status = postgre.signupUser(username, password, email)

    if status['status'] == 'ok':
        if postgre.autentithicateUser(username, password):
            session['username'] = username

    return jsonify(status)