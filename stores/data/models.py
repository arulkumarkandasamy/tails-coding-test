import json
import pandas as pd
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from stores import utils


db = SQLAlchemy()


def get_stores_from_json():
    with open('stores.json') as json_file:
        store_list = json.load(json_file)
        df = pd.DataFrame(store_list)
        current_app.logger.debug('Fetching Latitude and Longitude from postcodes.io')
        df['latitude'] = df.apply(lambda row: utils.get_lattitude(row.postcode), axis=1)
        df['longitude'] = df.apply(lambda row: utils.get_longitude(row.postcode), axis=1)
        df = df.sort_values(by=['name'])
        utils.format_index(df)
        current_app.logger.debug('Storing Dataframe in db')
        df.to_sql(name='stores', con=db.engine, index=False)
        return df


def get_stores_in_radius(radius, store_name, stores):
    sel_row = stores[stores['name'] == store_name].values
    sel_lat = sel_row[0][2]
    sel_lon = sel_row[0][3]
    if sel_lat == 0:
        raise Exception('Latitude is zero')
    current_app.logger.debug('Fetching stores within radius')
    stores['distance'] = stores.apply(lambda row: 0 if row['name'] == store_name \
        else utils.distance_calc(row, sel_lat, sel_lon), axis=1)
    stores_within_radius = stores[(stores['distance'] <= int(radius)) \
                                  & (stores['distance'] != 0)]
    stores_within_radius = \
        stores_within_radius.sort_values(by=['latitude'], ascending=False)
    current_app.logger.debug('Fetching stores within radius. Formatting index')
    utils.format_index(stores_within_radius)
    return stores_within_radius

def get_stores_from_db():
    current_app.logger.debug('Fecthing Dataframe from db')
    try:
        stores = pd.read_sql_query("select * from stores", db.engine)
    except exc.SQLAlchemyError:
        return None
    return stores
