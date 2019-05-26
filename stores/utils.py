import re
import postcodes_io_api
from geopy.distance import vincenty


def get_lattitude(postcode):
    postcode = re.sub(r"\s+", "", postcode)
    data = get_data_for_postcode(postcode)
    return data.get("result").get("latitude")

def get_longitude(postcode):
    postcode = re.sub(r"\s+", "", postcode)
    data = get_data_for_postcode(postcode)
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