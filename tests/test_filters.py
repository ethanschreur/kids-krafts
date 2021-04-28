from unittest import TestCase
import app.filters as filters

class FiltersFileTestCase(TestCase):
    def test_filter_products(self):
        class Product():
            def __init__(self, category):
                self.category = category
        prod_1 = Product("Selling")
        prod_2 = Product("Not Selling")
        prod_3 = Product("Not Selling")
        
        products = [prod_1, prod_2, prod_3]
        self.assertEqual(len(filters.filter_products('selling_status', 'selling', products)), 1)
        self.assertEqual(len(filters.filter_products('selling_status', 'not_selling', products)), 2)

    def test_filter_orders(self):
        class Order():
            def __init__(self, name, email, status, payment_type, payment_status):
                self.name = name
                self.email = email
                self.status = status
                self.payment_type = payment_type
                self.payment_status = payment_status
        order_1 = Order('C Name 1', 'Cname_1@gmail.com', 'ordered', 'stripe', 'paid')
        order_2 = Order('B Name 2', 'Bname_2@gmail.com', 'made', 'not stripe', 'not paid')
        order_3 = Order('A Name 3', 'Aname_3@gmail.com', 'fulfilled', 'stripe', 'paid')

        orders = [order_1, order_2, order_3]
        self.assertEqual(filters.filter_orders('name', '', orders), [order_3, order_2, order_1])
        self.assertEqual(filters.filter_orders('email', '', orders), [order_3, order_2, order_1])
        self.assertEqual(len(filters.filter_orders('order_status', 'made', orders)), 1)
        self.assertEqual(len(filters.filter_orders('payment_type', 'stripe', orders)), 2)
        self.assertEqual(len(filters.filter_orders('payment_status', 'paid', orders)), 2)

    def test_search_orders(self):
        class Order():
            def __init__(self, pickup_time, status):
                self.pickup_time = pickup_time
                self.status = status
        order_1 = Order('January 1 AM', 'made')
        order_2 = Order('February 1 AM', 'made')
        order_3 = Order('March 1 AM', 'fulfilled')

        orders = [order_1, order_2, order_3]
        self.assertEqual(len(filters.search_orders('pickup_time', 'February 1 AM', orders)), 1)
        self.assertEqual(len(filters.search_orders('pickup_time', 'March 1 AM', orders)), 0)
