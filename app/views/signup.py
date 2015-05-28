from flask import render_template, request, redirect, jsonify

from app import app
from app.db import postgre
from app.utils import hash, session

@app.route('/signup', methods=['GET'])
def signup_get():
    return render_template('signup.html', title = 'Ztd.Blunders')

@app.route('/signup', methods=['POST'])
def signup_post():
    username, password, email = request.json['username'], request.json['password'], request.json['email']

    salt, hashPass = hash.new(username, password)
    status = postgre.signupUser(username, salt, hashPass, email)

    if status['status'] == 'ok':
        session.authorize(username, password)

    return jsonify(status)