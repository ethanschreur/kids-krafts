from unittest import TestCase
from app import create_app
from models import db, Order, Purchase, Product, Subproduct
import datetime

class ModelsTestCase(TestCase):
    def setUp(self):
        # create the app testing environment
        create_app('TESTING')

        # delete and create tables
        db.drop_all()
        db.create_all()

        # add a product row and subproducts for that product
        craft1 = {'name': "Punxsutawney Phil", 'image_url': "../static/seed_images/kit_1/punxsutawney_phil.jpg"}
        craft2 = {'name': "Snowstorm Painting", 'image_url': "../static/seed_images/kit_1/snowstorm_painting.jpg"}
        craft3 = {'name': "valentine_pup", 'image_url': "../static/seed_images/kit_1/valentine_pup.jpg"}
        craft4 = {'name': "Marshmallow Snowman", 'image_url': "../static/seed_images/kit_1/marshmallow_snowman.jpg"}
        new_product = Product(name = "February Kit 21", price = 5.00, image_url = "../static/seed_images/kit_1/product_image.jpg", category = "not_selling")
        db.session.add(new_product)
        db.session.commit()
        new_craft1 = Subproduct(product_id = new_product.id, name = craft1["name"], image_url = craft1["image_url"])
        db.session.add(new_craft1)
        new_craft2 = Subproduct(product_id = new_product.id, name = craft2["name"], image_url = craft2["image_url"])
        db.session.add(new_craft2)
        new_craft3 = Subproduct(product_id = new_product.id, name = craft3["name"], image_url = craft3["image_url"])
        db.session.add(new_craft3)
        new_craft4 = Subproduct(product_id = new_product.id, name = craft4["name"], image_url = craft4["image_url"])
        db.session.add(new_craft4)
        db.session.commit()

        # add an order including one purchase row for two kits
        purchase = {'product_id': new_product.id, 'number_ordered': 2, 'number_made': 0}
        new_order = Order(stripe_order_id = "fakestripeid", first_name = "First", last_name = "Last", date_time = datetime.datetime.now(), email = "fake@gmail.com", status = "received", notes = "",)
        db.session.add(new_order)
        db.session.commit()
        new_purchase = Purchase(order_id = new_order.id, product_id = purchase["product_id"], number_ordered = purchase["number_ordered"], number_made = purchase["number_made"])
        db.session.add(new_purchase)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_product_row(self):
        # test the row for the added seller
        p = Product.query.filter_by(name = "February Kit 21").first()
        self.assertEqual(p.name, "February Kit 21")
        self.assertEqual(p.price, 5.00)
        self.assertEqual(p.image_url, "../static/seed_images/kit_1/product_image.jpg")
        self.assertEqual(p.category, "not_selling")
        self.assertEqual(len(p.subproducts), 4)

    def test_subproduct_row(self):
        # test the row for an added subproduct
        s = Subproduct.query.filter_by(name = "Punxsutawney Phil").first()
        self.assertEqual(s.name, "Punxsutawney Phil")
        self.assertEqual(s.image_url, "../static/seed_images/kit_1/punxsutawney_phil.jpg")
        self.assertEqual(s.product.name, "February Kit 21")

    def test_order_row(self):
        # test the row for the added order
        o = Order.query.filter_by(stripe_order_id = "fakestripeid").first()
        self.assertEqual(o.stripe_order_id, "fakestripeid")
        self.assertEqual(o.first_name, "First")
        self.assertEqual(o.last_name, "Last")
        self.assertEqual(type(o.date_time), datetime.datetime)
        self.assertEqual(o.email, "fake@gmail.com")
        self.assertEqual(o.status, "received")
        self.assertEqual(o.notes, "")
        self.assertEqual(len(o.purchases), 1)

    def test_purchase_row(self):
        # test the row for an added purchase
        prod = Product.query.filter_by(name = "February Kit 21").first()
        p = Purchase.query.filter_by(product_id = prod.id).first()
        self.assertEqual(type(p.order_id), int)
        self.assertEqual(p.product_id, prod.id)
        self.assertEqual(p.number_ordered, 2)
        self.assertEqual(p.number_made, 0)
        self.assertEqual(p.order.first_name, "First")

    def test_product_purchases_relationships(self):
        # test the relationships between a purchase and its product that is being purchased
        prod = Product.query.filter_by(name = "February Kit 21").first()
        purchases = prod.purchases
        self.assertEqual(len(purchases), 1)
        product = purchases[0].product
        self.assertEqual(product, prod)