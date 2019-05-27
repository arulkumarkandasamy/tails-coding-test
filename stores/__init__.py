from flask import abort, Flask, render_template, request, current_app
from stores.tails.controllers import main
from stores.cache import cache
from stores.config import configure_app
from stores.data.models import db

app = Flask(__name__,
            template_folder='templates')

configure_app(app)
cache.init_app(app)
db.init_app(app)

@app.errorhandler(404)
def page_not_found(error):
    current_app.logger.error('Page not found: %s', (request.path, error))
    return render_template('404.htm', error=error), 404


@app.errorhandler(500)
def internal_server_error(error):
    current_app.logger.error('Server Error: %s', (error))
    return render_template('500.htm', error=error), 500


@app.errorhandler(Exception)
def unhandled_exception(error):
    current_app.logger.error('Unhandled Exception: %s', (error))
    return render_template('500.htm', error=error), 500



@app.route('/')
def home():
    return render_template('index.htm')


app.register_blueprint(main, url_prefix='/tails')
