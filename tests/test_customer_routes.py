from unittest import TestCase
from app import create_app

class SellerRoutesTestCase(TestCase):
    def setUp(self):
        # create the app testing environment
        self.app = create_app('TESTING')
        self.client = self.app.test_client()

    def test_landing_page(self):
        with self.client as client:
            # test the landing page html
            resp = client.get('/')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('How It Works', resp.get_data(as_text=True))
            self.assertIn('People ❤️ Kids Krafts', resp.get_data(as_text=True))