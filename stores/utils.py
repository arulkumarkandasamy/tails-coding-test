import re
import postcodes_io_api
from geopy.distance import vincenty



def get_lattitude(postcode):
    data = get_data_for_postcode(postcode)
    if data['status'] == 404:
        latitude = 0
    else:
        latitude = data.get("result").get("latitude")
    return latitude

def get_longitude(postcode):
    data = get_data_for_postcode(postcode)
    if data['status'] == 404:
        longitude = 0
    else:
        longitude = data.get("result").get("longitude")
    return longitude

def get_data_for_postcode(postcode):
    # removing space in postcodes
    postcode = re.sub(r"\s+", "", postcode)
    api = postcodes_io_api.Api(debug_http=True)
    data = api.get_postcode(postcode)
    return data

def distance_calc(row, sel_lat, sel_lon):
    start = (sel_lat, sel_lon)
    stop = (row['latitude'], row['longitude'])
    # Caluclate disatnce between 2 points start and stop
    return vincenty(start, stop)

def format_index(stores):
    # resetting index
    stores.reset_index(inplace=True)
    # start index from 1
    stores.index += 1
    # drop index column in dataframe
    stores.drop("index", axis=1, inplace=True)
    return stores
