import unittest
from stores import app


class StoresTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/tails/stores')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_store_data(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/tails/stores_in_radius?radius=25&store_name=Reading')

        # assert the response data
        self.assertEqual(result.status_code, 200)
