from datetime import datetime

from flask import render_template
from app import app
from app.utils import session

@app.route('/')
@app.route('/index')
def main():
    return render_template('main.html', title = 'Ztd.Blunders', session = session)

@app.route('/helpus')
def helpus():
    return render_template('helpus.html', title = 'Help us', session = session)

@app.route('/termsOfUse')
def termsOfUse():
    return render_template(
        'termsOfUse.html',
        title = 'Terms of Use',
        year = datetime.now().year,
        session = session
    )

@app.route('/download')
def download():
    return render_template('download.html', title = 'Download', session = session)

@app.route('/api')
def api():
    return render_template('api.html', title = 'API', session = session)

@app.errorhandler(404)
def notFound(error):
    return render_template('404.html', title = '404', session = session)

@app.errorhandler(500)
@app.errorhandler(503)
def internalError(error):
    return render_template('50x.html', title = 'Something went wrong', session = session)
