from unittest import TestCase
from app import create_app
import os

class SellerRoutesTestCase(TestCase):
    def setUp(self):
        # create the app testing environment
        self.app = create_app('TESTING')
        self.client = self.app.test_client()

        # define some useful class variables
        self.product_data = {'product_image': [open('static/images/bluebird.png', 'rb')], 'product_name': 'Easter Kit', 'product_price': '5.99', 'product_selling_status': 'Not Selling'}
        self.subproduct_data = {'subproduct_image': [open('static/images/bluebird.png', 'rb')],'subproduct_name': 'name'}
        self.order_data = {'order_name': 'Ethan Schreur', 'order_pickup_time': 'April 25 PM', 'order_email': 'ethanschreur@icloud.com', 'order_notes': 'these are notes'}
        self.purchase_data = {'product_id': 1, 'number_ordered': 2}

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
            self.assertIn('Seller Dashboard', resp.get_data(as_text=True))

            # test going to login page while seler_email is in the session
            resp = client.get('/login', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Seller Dashboard', resp.get_data(as_text=True))

            # test logging out and then logging in with wrong credentials
            client.get('/logout')
            resp = client.post('/login', data={"email": "wrong@gmail.com", "password": "qwerty"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Submit', resp.get_data(as_text=True))

            # test logging in with uppercase and spaces at the beginning and end
            resp = client.post('/login', data={'email': '   '+os.environ.get('seller_email').upper()+'  ', 'password': '  '+os.environ.get('seller_password').upper()+'  '}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Seller Dashboard', resp.get_data(as_text=True))

    def test_dashboard(self):
        with self.client as client:
            # test going to dashboard with seller_email NOT in session
            client.get('/logout')
            resp = client.get('/dashboard', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Seller Dashboard', resp.get_data(as_text=True))

            # test going to dashboard with seller_email in session
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password': os.environ.get('seller_password')})
            resp = client.get('/dashboard', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Seller Dashboard', resp.get_data(as_text=True))

    def test_products(self):
        with self.client as client:
            # test going to the products with seller_email NOT in session
            client.get('/logout')
            resp = client.get('/products', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Add a Product', resp.get_data(as_text=True))
            self.assertNotIn('<h2>Products</h2>', resp.get_data(as_text=True))

            # test going to the products with seller_email in session
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password': os.environ.get('seller_password')})
            resp=client.get('/products', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add a Product', resp.get_data(as_text=True))
            self.assertIn('<h2>Products</h2>', resp.get_data(as_text=True))

            # test going to the products with a filter
            resp = client.get('/products?order_by=selling_status&value=selling', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            # test submitting the add-product form with seller_email in session
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password':os.environ.get('seller_password')})
            resp=client.post('/products', follow_redirects=True, data=self.product_data, content_type='multipart/form-data')
            self.assertIn('Add a Product', resp.get_data(as_text=True))
            self.assertIn('<h2>Products</h2>', resp.get_data(as_text=True))
            self.assertIn('Easter Kit', resp.get_data(as_text=True))
            self.assertIn('5.99', resp.get_data(as_text=True))
            self.assertIn('Not Selling', resp.get_data(as_text=True)) 

    def test_updating_products(self):
        with self.client as client:
            # test going to a product with seller_email not in the session
            client.get('/logout')
            resp = client.get('/products/1', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Edit Product', resp.get_data(as_text=True))
            self.assertNotIn('Add a Subproduct', resp.get_data(as_text=True))
            self.assertNotIn('Edit Subproducts', resp.get_data(as_text=True))

            # test going to a product page with seller_email in the session
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password':os.environ.get('seller_password')})
            resp = client.get('/products/1', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit Product', resp.get_data(as_text=True))
            self.assertIn('Add a Subproduct', resp.get_data(as_text=True))
            self.assertIn('Edit Subproducts', resp.get_data(as_text=True))

            # test editting a product with seller_email in the session
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password':os.environ.get('seller_password')})
            resp = client.post('/products/1', follow_redirects=True, data={'product_image': [open('static/images/bluebird.png', 'rb')], 'product_name': 'Editted Name', 'product_price': '999.99', 'product_selling_status': 'Selling'}, content_type='multipart/form-data')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit Product', resp.get_data(as_text=True))
            self.assertIn('Add a Subproduct', resp.get_data(as_text=True))
            self.assertIn('Edit Subproducts', resp.get_data(as_text=True))
            self.assertIn('Editted Name', resp.get_data(as_text=True))
            self.assertIn('999.99', resp.get_data(as_text=True))

            # test deleting a product with seller_email not in the session
            client.get('/logout')
            resp = client.get('/products/1/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Edit Product', resp.get_data(as_text=True))
            self.assertNotIn('Add a Subproduct', resp.get_data(as_text=True))
            self.assertNotIn('Edit Subproducts', resp.get_data(as_text=True))

            # test deleting a product with seller_email in the sesison
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password':os.environ.get('seller_password')})
            resp = client.get('/products/1/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add a Product', resp.get_data(as_text=True))
            self.assertIn('<h2>Products</h2>', resp.get_data(as_text=True))
            resp = client.get('/products/1', follow_redirects=True)
            self.assertNotEqual(resp.status_code, 200)

            # test adding a subproduct with seller_email in the session
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password':os.environ.get('seller_password')})
            resp = client.post('/products/2/subproducts', data=self.subproduct_data, follow_redirects=True, content_type='multipart/form-data')
            self.assertEqual(200, resp.status_code)
            self.assertIn('Edit Product', resp.get_data(as_text=True))
            self.assertIn('Add a Subproduct', resp.get_data(as_text=True))
            self.assertIn('Edit Subproducts', resp.get_data(as_text=True))
            self.assertIn(self.subproduct_data['subproduct_name'], resp.get_data(as_text=True))

            # test editting a subproduct with seller_email in the session
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password':os.environ.get('seller_password')})
            resp = client.post('/products/2/subproducts/5', follow_redirects=True, data={'subproduct_name': 'Editted Name', 'subproduct_image': [open('static/images/bluebird.png', 'rb')]}, content_type='multipart/form-data')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Editted Name', resp.get_data(as_text=True))

            # test deleting a subproduct with seller_email not in the session
            client.get('/logout')
            resp = client.get('/products/2/subproducts/5/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Edit Product', resp.get_data(as_text=True))
            self.assertNotIn('Add a Subproduct', resp.get_data(as_text=True))
            self.assertNotIn('Edit Subproducts', resp.get_data(as_text=True))

            # test deleting a subproduct with seller_email in the session
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password':os.environ.get('seller_password')})
            resp = client.get('/products/2/subproducts/5/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Editted Name', resp.get_data(as_text=True))
            self.assertNotIn('Editted Link', resp.get_data(as_text=True))


    def test_orders(self):
        with self.client as client:
            # test going to the orders with seller_email NOT in session
            client.get('/logout')
            resp = client.get('/orders', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('<h2>Orders</h2>', resp.get_data(as_text=True))

            # test going to the orders with seller_email in session
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password': os.environ.get('seller_password')})
            resp=client.get('/orders', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Orders</h2>', resp.get_data(as_text=True))

            # test going to the products with filters
            resp = client.get('/orders?order_by=order_status&value=made', follow_redirects =True)
            self.assertEqual(resp.status_code, 200)
            resp = client.get('/orders?pickup_time=April+2+AM', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            resp = client.get('/orders?order_by=name', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

             # test submitting the add-orders form with seller_email NOT in session
            client.get('/logout')
            resp = client.post('/orders', follow_redirects=True, data=self.order_data) 
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Add an Order', resp.get_data(as_text=True))
            self.assertNotIn('<h2>Orders</h2>', resp.get_data(as_text=True))

            # test submitting the add-orders form with seller_email in session
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password':os.environ.get('seller_password')})
            resp=client.post('/orders', follow_redirects=True, data=self.order_data)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add an Order', resp.get_data(as_text=True))
            self.assertIn('<h2>Orders</h2>', resp.get_data(as_text=True))
            self.assertIn('Ethan Schreur', resp.get_data(as_text=True))
            self.assertIn('ethanschreur@icloud.com', resp.get_data(as_text=True))
            self.assertIn('April 25 PM', resp.get_data(as_text=True))
            self.assertIn('these are notes', resp.get_data(as_text=True))
        
    def test_updating_orders(self):
        with self.client as client:
            # test going to an order with seller_email not in the session
            client.get('/logout')
            resp = client.get('/orders/1', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Edit Order', resp.get_data(as_text=True))

            # test going to an order page with seller_email in the session
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password':os.environ.get('seller_password')})
            resp = client.get('/orders/1', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit Order', resp.get_data(as_text=True))

            # # test editting an order with seller_email not in the session
            client.get('/logout')
            resp = client.post('/orders/1', follow_redirects=True, data={'order_stripe_order_id': '123', 'order_name': 'Edited Name', 'order_pickup_time': 'April 24 AM', 'order_email': 'kidskrafts4u@gmail.com', 'order_status': 'ordered', 'order_payment_type': 'stripe', 'order_payment_status': 'paid', 'order_notes': 'edit notes'})
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Edit Order', resp.get_data(as_text=True))
   
            # test editting an order with seller_email in the session
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password':os.environ.get('seller_password')})
            resp = client.post('/orders/1', follow_redirects=True, data={'order_stripe_order_id': '123', 'order_name': 'Edited Name', 'order_pickup_time': 'April 24 AM', 'order_email': 'kidskrafts4u@gmail.com', 'order_status': 'ordered', 'order_payment_type': 'stripe', 'order_payment_status': 'paid', 'order_notes': 'edit notes'})
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit Order', resp.get_data(as_text=True))
            self.assertIn('123', resp.get_data(as_text=True))
            self.assertIn('Edited Name', resp.get_data(as_text=True))
            self.assertIn('kidskrafts4u@gmail.com', resp.get_data(as_text=True))

            # test deleting an order with seller_email not in the session
            client.get('/logout')
            resp = client.get('/orders/1/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Edit Order', resp.get_data(as_text=True))

            # test deleting an order with seller_email in the sesison
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password':os.environ.get('seller_password')})
            resp = client.get('/orders/1/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add an Order', resp.get_data(as_text=True))
            self.assertIn('<h2>Orders</h2>', resp.get_data(as_text=True))
            resp = client.get('/orders/1', follow_redirects=True)
            self.assertNotEqual(resp.status_code, 200)

            # test adding a purchase with seller_email in the session
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password':os.environ.get('seller_password')})
            resp = client.post('/orders/2/purchases', data=self.purchase_data, follow_redirects=True)
            self.assertEqual(200, resp.status_code)
            self.assertIn('Edit Order', resp.get_data(as_text=True))
            self.assertIn('Add a Purchase', resp.get_data(as_text=True))
            self.assertIn('Edit Purchases', resp.get_data(as_text=True))
            self.assertIn('February Kit 21', resp.get_data(as_text=True))

            # test editting a purchase with seller_email not in the session
            client.get('/logout')
            resp = client.post('/orders/2/purchases/2', follow_redirects=True, data={'number_ordered': 8, 'number_made': 8})
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('value="8"', resp.get_data(as_text=True))

            # test editting a purchase with seller_email in the session
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password':os.environ.get('seller_password')})
            resp = client.post('/orders/2/purchases/2', follow_redirects=True, data={'number_ordered': 8, 'number_made': 8})
            self.assertEqual(resp.status_code, 200)
            self.assertIn('value="8"', resp.get_data(as_text=True))

            # test deleting a purchase with seller_email not in the session
            client.get('/logout')
            resp = client.get('/orders/2/purchases/2/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Login', resp.get_data(as_text=True))

            # test deleting a purchase with seller_email in the session
            client.post('/login', data={'email':os.environ.get('seller_email'), 'password':os.environ.get('seller_password')})
            resp = client.get('/orders/2/purchases/2/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('<pan>February Kit 21</span>', resp.get_data(as_text=True))
