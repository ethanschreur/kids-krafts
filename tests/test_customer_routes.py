from unittest import TestCase
from app import create_app

class SellerRoutesTestCase(TestCase):
    def setUp(self):
        # create the app testing environment
        self.app = create_app('TESTING')
        self.client = self.app.test_client()

    def test_home_route(self):
        # test the home/landing page route
        with self.client as client:
            res = client.get('/')
            self.assertEqual(res.status_code, 200)