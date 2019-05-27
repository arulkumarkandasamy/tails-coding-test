import pandas as pd
from flask import Blueprint, current_app, render_template, request
from stores.cache import cache
from stores.data import models
from stores import utils


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/stores')
@cache.cached(300)
def get_stores():
    store_data = cache.get('stores_data')
    if store_data is not None:
        stores_json = pd.io.json.read_json(store_data)
        stores = pd.DataFrame(stores_json)
        utils.format_index(stores)
    else:
        stores = models.get_stores_from_db()
        if stores is not None:
            utils.format_index(stores)
        else:
            stores = models.get_stores_from_json()
            cache.set('stores_data', stores.to_json())
    current_app.logger.debug('Displaying all stores')
    return render_template('stores.html', stores=[stores.to_html(classes='store')])

@main.route('/stores_in_radius')
def get_tores_in_radius():
    radius = request.args.get('radius')
    store_name = request.args.get('store_name')
    store_data = cache.get('stores_data')
    if store_data is not None:
        stores_json = pd.io.json.read_json(store_data)
        stores = pd.DataFrame(stores_json)
        utils.format_index(stores)
    else:
        stores = models.get_stores_from_db()
        if stores is not None:
            utils.format_index(stores)
        else:
            stores = models.get_stores_from_json()
            cache.set('stores_data', stores.to_json())
    stores = stores[['name', 'postcode', 'latitude', 'longitude']]
    stores_in_radius = models.get_stores_in_radius(radius, store_name, stores)
    current_app.logger.debug('Displaying stores within %s km radius from %s ' %(radius, store_name))
    return render_template('stores.html', stores=[stores_in_radius.to_html(classes='store')])
