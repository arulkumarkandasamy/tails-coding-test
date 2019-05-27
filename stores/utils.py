import re
import postcodes_io_api
from geopy.distance import vincenty
from flask import current_app


def get_lattitude(postcode):
    postcode = re.sub(r"\s+", "", postcode)
    current_app.logger.debug('Utils Getting Latitude from postcodes.io')
    try:
        data = get_data_for_postcode(postcode)
        if data['status'] == 404:
            return 0
    except IOError:
        return 0
    return data.get("result").get("latitude")

def get_longitude(postcode):
    postcode = re.sub(r"\s+", "", postcode)
    current_app.logger.debug('Utils Getting Longitude from postcodes.io')
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
    current_app.logger.debug('Utils Calculate distance from latitude and longitude')
    start = (sel_lat, sel_lon)
    stop = (row['latitude'], row['longitude'])
    return vincenty(start, stop)

def format_index(stores):
    current_app.logger.debug('Utils Formatting index')
    stores.reset_index(inplace=True)
    stores.index += 1
    stores.drop("index", axis=1, inplace=True)
    return stores
