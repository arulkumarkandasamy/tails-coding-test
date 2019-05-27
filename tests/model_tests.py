import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
from stores.data import models
from stores import utils



class ModelTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # inputs
        self.radius = 15
        self.store_name = "Hatfield"
        self.stores = pd.DataFrame(
            {'name':
                 ['Hertford', 'St_Albans', 'Borehamwood', 'Dunstable', 'Luton', \
                  'Hemel_Hempstead', 'Waltham_Abbey', 'Enfield', 'Watford', 'Hatfield'],
             'postcode':
                 ['SG13 7RQ', 'AL1 2RJ', 'WD6 4PR', 'LU5 4XZ', 'LU1 3JH', 'HP3 9AA',\
                  'EN9 1BY', 'EN1 1TH', 'WD17 2SF', 'AL9 5JP'],
             'latitude':
                 [51.797063, 51.741753, 51.656694, 51.890604, 51.873519, 51.739299, \
                  51.686020, 51.653761, 51.649103, 51.776142],
             'longitude':
                 [-0.069212, -0.341337, -0.277805, -0.514047, -0.398200, -0.474067, \
                  -0.009966, -0.054651, -0.389487, -0.222034]}
        )
        self.stores = self.stores[['name', 'postcode', 'latitude', 'longitude']]

        # expected output
        self.stores_within_radius = pd.DataFrame(
            {'name':
                 ['Hertford', 'St_Albans', 'Borehamwood'],
             'postcode':
                 ['SG13 7RQ', 'AL1 2RJ', 'WD6 4PR'],
             'latitude':
                 [51.797063, 51.741753, 51.656694],
             'longitude':
                 [-0.069212, -0.341337, -0.277805]}
        )
        self.stores_within_radius = utils.format_index(self.stores_within_radius)
        self.stores_within_radius = self.stores_within_radius[['name', 'postcode',\
                                                               'latitude', 'longitude']]


    def tearDown(self):
        pass

    def test_stores_within_radius(self):
        expected = self.stores_within_radius
        actual = models.get_stores_in_radius(self.radius, self.store_name, self.stores)
        actual.drop("distance", axis=1, inplace=True)
        assert_frame_equal(expected, actual)

    def test_stores_distance_within_radius(self):
        expected_count = 0
        actual = models.get_stores_in_radius(self.radius, self.store_name, self.stores)
        seriesObj = actual.apply(lambda x: True if x['distance'] > 15 else False, axis=1)
        actual_count = len(seriesObj[seriesObj].index)
        self.assertEqual(expected_count, actual_count)

    def test_stores_within_radius_north_south(self):
        actual = models.get_stores_in_radius(self.radius, self.store_name, self.stores)
        expected = actual.sort_values(by='latitude', ascending=False)
        assert_frame_equal(expected, actual)
