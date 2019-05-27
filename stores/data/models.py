import json
import pandas as pd
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from stores.cache import cache
from stores import utils

db = SQLAlchemy()


def get_stores_data():
    store_data = cache.get('stores_data')
    if store_data is not None:
        stores_json = pd.io.json.read_json(store_data)
        stores = pd.DataFrame(stores_json)
        utils.format_index(stores)
    else:
        # Getting stores data from db
        stores = get_stores_from_db()
        if stores is not None:
            utils.format_index(stores)
        else:
            # Getting stores data from stroes.json file
            stores = get_stores_from_json()
            cache.set('stores_data', stores.to_json())
    stores = stores.sort_values(by=['name'])
    utils.format_index(stores)
    stores = stores[['name', 'postcode', 'latitude', 'longitude']]
    return stores

def get_stores_from_json():
    with open('stores.json') as json_file:
        store_list = json.load(json_file)
        stores = pd.DataFrame(store_list)
        stores['latitude'] = stores.apply(lambda row: utils.get_lattitude(row.postcode), axis=1)
        stores['longitude'] = stores.apply(lambda row: utils.get_longitude(row.postcode), axis=1)
        stores.to_sql(name='stores', con=db.engine, index=False)
        return stores

def get_stores_in_radius(radius, store_name, stores):
    # Ordering dataframe column as column order may be different while fetching dataframes
    stores = stores[['name', 'postcode', 'latitude', 'longitude']]
    sel_row = stores[stores['name'] == store_name].values
    sel_lat = sel_row[0][2]
    sel_lon = sel_row[0][3]
    if sel_lat == 0:
        raise Exception('Latitude is zero')
    # Calculating disatnce for each row of the dataframe
    stores['distance'] = stores.apply(lambda row: 0 if row['name'] == store_name \
        else utils.distance_calc(row, sel_lat, sel_lon), axis=1)
    # Filtering dataframe with radius less than given radius and
    #  disatnce not equal 0 (to exclude same store given in request)
    stores_within_radius = stores[(stores['distance'] <= int(radius)) \
                                  & (stores['distance'] != 0)]
    # Sorting dataframe with northmost store on top
    stores_within_radius = \
        stores_within_radius.sort_values(by=['latitude'], ascending=False)
    # Formatting index
    utils.format_index(stores_within_radius)
    return stores_within_radius

def get_stores_from_db():
    try:
        # populate datafrom by querying from db
        stores = pd.read_sql_query("select * from stores", db.engine)
    except exc.SQLAlchemyError:
        return None
    return stores
