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