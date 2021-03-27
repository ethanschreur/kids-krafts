from unittest import TestCase
from app import create_app
import os

class SellerRoutesTestCase(TestCase):
    def setUp(self):
        # create the app testing environment
        self.app = create_app('TESTING')
        self.client = self.app.test_client()
        


    def test_login_and_logout(self):
        with self.client as client:
            # test the login page html
            resp = client.get('/login')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Email', resp.get_data(as_text=True))
            self.assertIn('Password', resp.get_data(as_text=True))
            self.assertIn('Submit', resp.get_data(as_text=True))

            # test logging in without seller_email being in the session
            resp = client.post(
                '/login',
                data={'email': os.environ.get('seller_email'), 'password': os.environ.get('seller_password')},
                follow_redirects=True
            )
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Dashboard', resp.get_data(as_text=True))

            # test going to login page while seler_email is in the session
            resp = client.get('/login', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Dashboard', resp.get_data(as_text=True))

            # test logging out and then logging in with wrong credentials
            client.get('/logout')
            resp = client.post('/login', data={"email": "wrong@gmail.com", "password": "qwerty"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Submit', resp.get_data(as_text=True))

            # test logging in with uppercase and spaces at the beginning and end
            resp = client.post('/login', data={'email': '   '+os.environ.get('seller_email').upper()+'  ', 'password': '  '+os.environ.get('seller_password').upper()+'  '}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Dashboard', resp.get_data(as_text=True))

    def test_dashboard(self):
        with self.client as client:
            # test going to dashboard with seller_email NOT in session
            client.get('/logout')
            resp = client.get('/dashboard', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Dashboard', resp.get_data(as_text=True))

            # test going to dashboard with seller_email in session
            client.post('/login', data={'email':'kidskrafts@gmail.com', 'password': 'abc123'})
            resp = client.get('/dashboard', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Dashboard', resp.get_data(as_text=True))

