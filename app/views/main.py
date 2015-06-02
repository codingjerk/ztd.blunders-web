from datetime import datetime

from flask import render_template
from app import app
from app.utils import session

@app.route('/faq')
def faq():
    return render_template('faq.html', title = 'FAQ', session = session)

@app.route('/about')
def about():
    return render_template('about.html', title = 'About', session = session)

@app.route('/donate')
def donate():
    return render_template('donate.html', title = 'Donate', session = session)

@app.route('/termsOfUse')
def termsOfUse():
    return render_template('termsOfUse.html', title = 'Terms of Use', year = datetime.now().year, session = session)