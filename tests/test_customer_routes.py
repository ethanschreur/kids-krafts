from unittest import TestCase
from app import create_app
import os
import json

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
            client.post('/products', follow_redirects=True, data=self.product_data_not_selling)
            resp = client.get('/shop')
            self.assertEqual(200, resp.status_code)
        
            # dont display products with the category "Not Selling"
            self.assertNotIn('Not Selling', resp.get_data(as_text=True))

            # display products with the category "Selling"
            self.assertIn('Selling', resp.get_data(as_text=True))

            # test what the product display looks like while the product data are not in session
            resp = client.get('/shop')
            self.assertEqual(200, resp.status_code)
            self.assertNotIn('check', resp.get_data(as_text=True))

            # test what the products display looks like while the product data are in session
            with client.session_transaction() as session:
                session['cart'] = {'1':{}}
            resp = client.get('/shop')
            self.assertEqual(200, resp.status_code)
            self.assertIn('check', resp.get_data(as_text=True))

    def test_cart_page(self):
        with self.client as client:
            with client.session_transaction() as session:
                session['cart'] = {}
            client.post('/cart', json={'id': '1', 'name': self.product_data_selling['product_name'], 'price': self.product_data_selling['product_price'], 'image': self.product_data_selling['product_image']}, content_type='application/json')
            resp = client.get('/cart')
            self.assertEqual(200, resp.status_code)
            self.assertIn(self.product_data_selling['product_name'], resp.get_data(as_text=True))
            client.post('/cart/remove', json={"id": '1'})
            resp = client.get('/cart')
            self.assertEqual(200, resp.status_code)
            self.assertNotIn(self.product_data_selling['product_name'], resp.get_data(as_text=True))

    def test_contact_page(self):
        with self.client as client:
            # test the contact page
            resp = client.get('/contact')
            self.assertEqual(200, resp.status_code)
            self.assertIn('Contact Us', resp.get_data(as_text=True))
            self.assertIn('Name', resp.get_data(as_text=True))
            self.assertIn('Email', resp.get_data(as_text=True))
            self.assertIn('Subject', resp.get_data(as_text=True))
            self.assertIn('Message', resp.get_data(as_text=True))
            # test submitting the contact form
            resp = client.post('/contact', data={'name': 'name', 'email': 'contact.kidskrafts4u@gmail.com', 'subject': 'Testing', 'message': 'This is a test.'}, follow_redirects=True)
            self.assertEqual(200, resp.status_code)
            self.assertIn('Your message was successfully sent', resp.get_data(as_text=True))
            
            # test going to the contact page with shipping = true in request args but no cart in session
            resp = client.get('/contact?shipping=true')
            self.assertEqual(200, resp.status_code)
            self.assertNotIn('Order', resp.get_data(as_text=True))
            self.assertNotIn('Total', resp.get_data(as_text=True))
            self.assertNotIn('Shipping Address', resp.get_data(as_text=True))
            self.assertNotIn('Notes', resp.get_data(as_text=True))

            # test going to the contact page with shipping = true in request args but an empty cart in session
            with client.session_transaction() as session:
                session['cart'] = {}
            resp = client.get('/contact?shipping=true')
            self.assertEqual(200, resp.status_code)
            self.assertNotIn('Order', resp.get_data(as_text=True))
            self.assertNotIn('Total', resp.get_data(as_text=True))
            self.assertNotIn('Shipping Address', resp.get_data(as_text=True))
            self.assertNotIn('Notes', resp.get_data(as_text=True))

            # test going to the contact page with shipping = true in request args with cart in session
            with client.session_transaction() as session:
                session['cart'] = {'1': {'name': 'kit_name', 'amount': 5}}
                session['total'] = 10.99
            # try changing the amount
            client.post('/cart/amount', json={ 'id': 1, 'amount': 6})
            resp = client.get('/contact?shipping=true')
            self.assertEqual(200, resp.status_code)
            self.assertIn('Order', resp.get_data(as_text=True))
            self.assertIn('Total', resp.get_data(as_text=True))
            self.assertIn('Shipping Address', resp.get_data(as_text=True))
            self.assertIn('Notes', resp.get_data(as_text=True))
            self.assertIn("[&#39;kit_name&#39;, 6]", resp.get_data(as_text=True))

    def test_about_page(self):
        with self.client as client:
            resp = client.get('/about')
            self.assertEqual(200, resp.status_code)
            self.assertIn('Kendra Schreur', resp.get_data(as_text=True))
            self.assertIn('Sharon Schreur', resp.get_data(as_text=True))
            self.assertIn('About Us', resp.get_data(as_text=True))
            self.assertIn('Social', resp.get_data(as_text=True))

    def test_order_details_page(self):
        with self.client as client:
            resp = client.get('/order_details')
            self.assertEqual(200, resp.status_code)
            self.assertIn('Order Details', resp.get_data(as_text=True))
            self.assertIn('Choose a Pickup Time', resp.get_data(as_text=True))
            self.assertIn('Pay', resp.get_data(as_text=True))

    def test_payment_process_and_success_page(self):
        with self.client as client:
            with client.session_transaction() as session:
                session['cart'] = {}
            client.post('/cart', json={'id': '1', 'name': self.product_data_selling['product_name'], 'price': self.product_data_selling['product_price'], 'image': self.product_data_selling['product_image']}, content_type='application/json')
            resp = client.get('/cart')
            resp = client.post('/create-checkout-session', json={'pickup': '25 AM', 'month': 'April'})
            session_id = (json.loads(resp.get_data())['id'])
            self.assertEqual(type(json.loads(resp.get_data())['id']), str)
            resp = client.get(f'/success?{session_id}')
            self.assertEqual(302, resp.status_code)