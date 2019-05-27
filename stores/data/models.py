import re
import json
import postcodes_io_api
import pandas as pd
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from geopy.distance import vincenty
from stores.cache import cache


db = SQLAlchemy()


def get_stores_data():
    store_data = cache.get('stores_data')
    if store_data is not None:
        stores_json = pd.io.json.read_json(store_data)
        stores = pd.DataFrame(stores_json)
        format_index(stores)
    else:
        # Getting stores data from db
        stores = get_stores_from_db()
        if stores is not None:
            format_index(stores)
        else:
            # Getting stores data from stroes.json file
            stores = get_stores_from_json()
            cache.set('stores_data', stores.to_json())
    return stores

def get_stores_from_json():
    with open('stores.json') as json_file:
        store_list = json.load(json_file)
        df = pd.DataFrame(store_list)
        df['latitude'] = df.apply(lambda row: get_lattitude(row.postcode), axis=1)
        df['longitude'] = df.apply(lambda row: get_longitude(row.postcode), axis=1)
        df = df.sort_values(by=['name'])
        format_index(df)
        df.to_sql(name='stores', con=db.engine, index=False)
        return df

def get_stores_in_radius(radius, store_name, stores):
    # Ordering dataframe column as column order may be different while fetching dataframes
    stores = stores[['name', 'postcode', 'latitude', 'longitude']]
    sel_row = stores[stores['name'] == store_name].values
    sel_lat = sel_row[0][2]
    sel_lon = sel_row[0][3]
    if sel_lat == 0:
        raise Exception('Latitude is zero')
    stores['distance'] = stores.apply(lambda row: 0 if row['name'] == store_name \
        else distance_calc(row, sel_lat, sel_lon), axis=1)
    stores_within_radius = stores[(stores['distance'] <= int(radius)) \
                                  & (stores['distance'] != 0)]
    stores_within_radius = \
        stores_within_radius.sort_values(by=['latitude'], ascending=False)
    format_index(stores_within_radius)
    return stores_within_radius

def get_lattitude(postcode):
    postcode = re.sub(r"\s+", "", postcode)
    try:
        data = get_data_for_postcode(postcode)
        if data['status'] == 404:
            return 0
    except IOError:
        return 0
    return data.get("result").get("latitude")

def get_longitude(postcode):
    postcode = re.sub(r"\s+", "", postcode)
    try:
        data = get_data_for_postcode(postcode)
        if data['status'] == 404:
            return 0
    except IOError:
        return 0
    return data.get("result").get("longitude")

def get_data_for_postcode(postcode):
    api = postcodes_io_api.Api(debug_http=True)
    return api.get_postcode(postcode)

def distance_calc(row, sel_lat, sel_lon):
    start = (sel_lat, sel_lon)
    stop = (row['latitude'], row['longitude'])
    return vincenty(start, stop)

def format_index(stores):
    stores.reset_index(inplace=True)
    stores.index += 1
    stores.drop("index", axis=1, inplace=True)
    return stores

def get_stores_from_db():
    try:
        stores = pd.read_sql_query("select * from stores", db.engine)
    except exc.SQLAlchemyError:
        return None
    return stores
