from datetime import datetime
from flask import render_template

from app import app
from app.api import getRandomBlunder

@app.route('/')
@app.route('/index')
def index():
    return render_template('training.html', title = 'Ztd.Blunders')

@app.route('/faq')
def faq():
    return render_template('faq.html', title = 'FAQ')

@app.route('/about')
def about():
    return render_template('about.html', title = 'About')

@app.route('/donate')
def donate():
    return render_template('donate.html', title = 'Donate')

@app.route('/termsOfUse')
def termsOfUse():
    return render_template('termsOfUse.html', title = 'Terms of Use', year = datetime.now().year)