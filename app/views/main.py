from datetime import datetime

from flask import render_template
from app import app
from app.utils import session,const

@app.route('/')
@app.route('/index')
def main():
    return render_template('main.html', title = const.app.title, session = session)

@app.route('/helpus')
def helpus():
    return render_template('helpus.html', title = '%s - Help us' % const.app.name, session = session)

@app.route('/termsOfUse')
def termsOfUse():
    return render_template(
        'termsOfUse.html',
        title = '%s - Terms of Use' % const.app.name,
        year = datetime.now().year,
        session = session
    )

@app.route('/privacy')
def privacy():
    return render_template(
        'privacy.html',
        title = '%s - Privacy policy' % const.app.name,
        session = session
    )

@app.route('/download')
def download():
    return render_template('download.html', title = '%s - Download' % const.app.name, session = session)

@app.route('/api')
def api():
    return render_template('api.html', title = '%s - API' % const.app.name, session = session)

@app.route('/faq')
def faq():
    return render_template('faq.html', title = '%s - FAQ' % const.app.name, session = session)

@app.errorhandler(404)
def notFound(error): #pylint: disable=unused-argument
    return render_template('404.html', title = 'Oops! Error 404', session = session)

@app.errorhandler(500)
@app.errorhandler(503)
def internalError(error): #pylint: disable=unused-argument
    return render_template('50x.html', title = 'Something went wrong', session = session)
