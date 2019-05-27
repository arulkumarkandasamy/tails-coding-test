from flask import Blueprint, current_app, render_template, request
from stores.cache import cache
from stores.data import models


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/stores')
@cache.cached(300)
def get_stores():
    # Getting stores data from cache
    stores = models.get_stores_data()
    current_app.logger.debug('Displaying all stores')
    return render_template('stores.html', stores=[stores.to_html(classes='store')])

@main.route('/stores_in_radius')
def get_tores_in_radius():
    radius = request.args.get('radius')
    store_name = request.args.get('store_name')
    stores = models.get_stores_data()
    # Getting stores data within the given radius of given store
    stores_in_radius = models.get_stores_in_radius(radius, store_name, stores)
    current_app.logger.debug('Displaying stores within %s km radius from %s ' %(radius, store_name))
    return render_template('stores.html', stores=[stores_in_radius.to_html(classes='store')])
