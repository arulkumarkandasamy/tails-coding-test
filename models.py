import json
import postcodes_io_api
import pandas as pd
from math import radians, cos, sin, asin, sqrt
from geopy.distance import vincenty
import re


class Stores():
    def get_stores_from_json(self):
        with open('stores.json') as json_file:
            store_list = json.load(json_file)
            df = pd.DataFrame(store_list)
            df['latitude'] = df.apply(lambda row: self.get_lattitude_from_postcode(row.postcode), axis=1)
            df['longitude'] = df.apply(lambda row: self.get_longitude_from_postcode(row.postcode), axis=1)
            df = df.sort_values(by=['name'])
            df.reset_index(inplace=True)
            df.index += 1
            df = df[['name','postcode','latitude','longitude']]
            print("new computed dataframe = ")
            print(df)
            return df

    def get_lattitude_from_postcode(self, postcode):
        postcode = re.sub(r"\s+", "", postcode)
        print('stripped postcode = \n', postcode)
        data = self.get_data_for_postcode(postcode)
        print("New Dataframe workflow")
        print(data)
        return data.get("result").get("latitude")

    def get_longitude_from_postcode(self, postcode):
        postcode = re.sub(r"\s+", "", postcode)
        print('stripped postcode = \n', postcode)
        data = self.get_data_for_postcode(postcode)
        return data.get("result").get("longitude")

    def get_data_for_postcode(self, postcode):
        api = postcodes_io_api.Api(debug_http=True)
        return api.get_postcode(postcode)

    def get_stores_in_radius(self,radius,store_name,stores):
        sel_row = stores[stores['name'] == store_name ].values
        sel_lat = sel_row[0][2]
        sel_lon = sel_row[0][3]
        print('sel_row latitude')
        print(sel_lat)
        print('sel_row longitude')
        print(sel_lon)
        stores['distance'] = stores.apply(lambda row: 0 if row['name'] == store_name else self.distance_calc(row, sel_lat, sel_lon), axis=1)
        print("radius : \n", radius)
        stores_within_radius = stores[(stores['distance'] <= int(radius)) & (stores['distance'] != 0)]
        stores_within_radius.reset_index(inplace=True)
        stores_within_radius.index += 1
        stores_within_radius = stores_within_radius[['name', 'postcode', 'latitude', 'longitude','distance']]
        return stores_within_radius

    def distance_calc(self,row,sel_lat, sel_lon):
        start = (sel_lat, sel_lon)
        stop = (row['latitude'], row['longitude'])
        print("start = ")
        print(start)
        print("stop = ")
        print(stop)
        return vincenty(start, stop)


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r