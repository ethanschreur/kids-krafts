from unittest import TestCase
from app import create_app
import os

class SellerRoutesTestCase(TestCase):
    def setUp(self):
        # create the app testing environment
        self.app = create_app('TESTING')
        self.client = self.app.test_client()

        # define some useful class variables
        self.product_data_selling = {'product_name': 'Selling', 'product_price': '5.99', 'product_image': 'https://scontent-ort2-2.xx.fbcdn.net/v/t1.0-9/165711988_218591189816105_7202222520073647668_o.jpg?_nc_cat=107&ccb=1-3&_nc_sid=730e14&_nc_ohc=THCcNKVPaEIAX9ltqbV&_nc_ht=scontent-ort2-2.xx&oh=85a30cd8715887c1d4e7111e499330e1&oe=6086013E', 'product_selling_status': 'Selling'}
        self.product_data_not_selling = {'product_name': 'Not Selling', 'product_price': '5.99', 'product_image': 'https://scontent-ort2-2.xx.fbcdn.net/v/t1.0-9/165711988_218591189816105_7202222520073647668_o.jpg?_nc_cat=107&ccb=1-3&_nc_sid=730e14&_nc_ohc=THCcNKVPaEIAX9ltqbV&_nc_ht=scontent-ort2-2.xx&oh=85a30cd8715887c1d4e7111e499330e1&oe=6086013E', 'product_selling_status': 'Not Selling'}
        self.subproduct_data = {'subproduct_name': 'name', 'subproduct_image': 'image'}

    def test_landing_page(self):
        with self.client as client:
            # test the landing page html
            resp = client.get('/')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('How It Works', resp.get_data(as_text=True))
            self.assertIn('People ❤️ Kids Krafts', resp.get_data(as_text=True))

    def test_shop_page(self):
        with self.client as client:
            # add two products with subproducts, one with the category "Not Selling", the other with category "Selling"
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password':os.environ.get('seller_password')})
            client.post('/products', follow_redirects=True, data=self.product_data_selling)
            client.post('/products/1/subproducts', data=self.subproduct_data, follow_redirects=True)
            client.post('/products', follow_redirects=True, data=self.product_data_not_selling)
            client.post('/products/1/subproducts', data=self.subproduct_data, follow_redirects=True)
            resp = client.get('/shop')
            self.assertEqual(200, resp.status_code)
           
            # dont display products with the category "Not Selling"
            self.assertNotIn('Not Selling', resp.get_data(as_text=True))

            # display products with the category "Selling"
            self.assertIn('Selling', resp.get_data(as_text=True))
