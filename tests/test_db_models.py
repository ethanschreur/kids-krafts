from unittest import TestCase
from app import app
from models import db, Order, Purchase, Product, Subproduct, Seller
import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///kids_krafts_test"
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

EMAIL = "KidsKrafts4U@gmail.com"
PASSWORD = "password"

class SellerModelTestCase(TestCase):
    def setUp(self):
        # delete and create tables
        db.drop_all()
        db.create_all()
        
        # add a seller row
        seller = Seller.register(EMAIL, PASSWORD)

    def tearDown(self):
        db.session.rollback()

    def test_seller_row(self):
        # test the row for the added seller
        u = Seller.query.filter_by(email = EMAIL).first()
        self.assertEqual(u.email, EMAIL)
        self.assertNotEqual(u.password, PASSWORD)
        
    def test_seller_registration(self):
        # test when registering a user should fail
        repeat_reg = Seller.register(EMAIL, PASSWORD)
        self.assertEqual(repeat_reg, False)
        
    def test_seller_authentication(self):
        # test authenticating the added seller
        correct_auth = Seller.authenticate(EMAIL, PASSWORD)
        self.assertNotEqual(correct_auth, False)
        incorrect_email_auth = Seller.authenticate("wrong@gmail.com", PASSWORD)
        self.assertEqual(incorrect_email_auth, False)
        incorrect_password_auth = Seller.authenticate(EMAIL, "wrong")
        self.assertEqual(incorrect_password_auth, False)
        incorrect_password_and_email_auth = Seller.authenticate('wrong@gmail.com', "wrong")
        self.assertEqual(incorrect_password_and_email_auth, False)

    def test_seller_edit(self):
        # test changing seller account email and/or password
        u = Seller.query.filter_by(email = EMAIL).first()
        edit = u.edit_seller("new_email@gmail.com", "new_password")
        self.assertEqual(edit, u)
        self.assertEqual(u.email, 'new_email@gmail.com')
        attempted_auth = Seller.authenticate("new_email@gmail.com", "new_password")
        self.assertNotEqual(attempted_auth, False)

    
class ProductModelTestCase(TestCase):
    def setUp(self):
        # delete and create tables
        db.drop_all()
        db.create_all()
        
        # add a product row and subproducts for that product
        subproducts = [{'name': "Punxsutawney Phil", 'image_url': "../static/seed_images/kit_1/punxsutawney_phil.jpg"}, {'name': "Snowstorm Painting", 'image_url': "../static/seed_images/kit_1/snowstorm_painting.jpg"}, {'name': "valentine_pup", 'image_url': "../static/seed_images/kit_1/valentine_pup.jpg"}, {'name': "Marshmallow Snowman", 'image_url': "../static/seed_images/kit_1/marshmallow_snowman.jpg"}]
        product = Product.add_product("February Kit 21", 5.00, "../static/seed_images/kit_1/product_image.jpg", "not_selling", subproducts)

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
    
    def test_product_edit(self):
        # test ing the product as well as the subproducts that are linked to the product
        p = Product.query.filter_by(name = "February Kit 21").first()
        subproducts = p.subproducts
        for sub in subproducts:
            sub.name = "edit"
        edit = p.edit_product("Edited Name", 10.00, "../static/seed_images/kit_1/edit_image.jpg", "selling", subproducts)
        self.assertEqual(p.name, 'Edited Name')
        self.assertEqual(p.price, 10.00)
        self.assertEqual(p.image_url, "../static/seed_images/kit_1/edit_image.jpg")
        self.assertEqual(p.category, "selling")
        edited_subs = Subproduct.query.filter_by(name = "edit").all()
        self.assertEqual(len(edited_subs), 4)

    def test_product_delete(self):
        # test deleting the product: the attatched subproducts should also be deleted
        p = Product.query.filter_by(name = "February Kit 21").first()
        id = p.id
        deleted = p.delete_product()
        self.assertEqual(deleted, True)
        no_subs = Subproduct.query.filter_by(product_id = id).first()
        self.assertEqual(no_subs, None)

class SubproductModelTestCase(TestCase):
    def setUp(self):
        # delete and create tables
        db.drop_all()
        db.create_all()
        
        # add a product row and subproducts for that product
        subproducts = [{'name': "Punxsutawney Phil", 'image_url': "../static/seed_images/kit_1/punxsutawney_phil.jpg"}, {'name': "Snowstorm Painting", 'image_url': "../static/seed_images/kit_1/snowstorm_painting.jpg"}, {'name': "valentine_pup", 'image_url': "../static/seed_images/kit_1/valentine_pup.jpg"}, {'name': "Marshmallow Snowman", 'image_url': "../static/seed_images/kit_1/marshmallow_snowman.jpg"}]
        product = Product.add_product("February Kit 21", 5.00, "../static/seed_images/kit_1/product_image.jpg", "not_selling", subproducts)

    def tearDown(self):
        db.session.rollback()

    def test_subproduct_row(self):
        # test the row for an added subproduct
        s = Subproduct.query.filter_by(name = "Punxsutawney Phil").first()
        self.assertEqual(s.name, "Punxsutawney Phil")
        self.assertEqual(s.image_url, "../static/seed_images/kit_1/punxsutawney_phil.jpg")
        self.assertEqual(s.product.name, "February Kit 21")

    def test_subproduct_edit(self):
        # test editing various parts of a subproduct
        s = Subproduct.query.filter_by(name = "Punxsutawney Phil").first()
        s.edit_subproduct(s.product_id, "new name", "new url")
        self.assertEqual(s.name, "new name")
        self.assertEqual(s.image_url, "new url")

    def test_subproduct_delete(self):
        # test delete one of the subproducts
        s = Subproduct.query.filter_by(name = 'Punxsutawney Phil').first()
        s.delete_subproduct()
        subs = Subproduct.query.all()
        self.assertEqual(len(subs), 3)


class OrderModelTestCase(TestCase):
    def setUp(self):
         # delete and create tables
        db.drop_all()
        db.create_all()
        
        # add a product row and subproducts for that product
        subproducts = [{'name': "Punxsutawney Phil", 'image_url': "../static/seed_images/kit_1/punxsutawney_phil.jpg"}, {'name': "Snowstorm Painting", 'image_url': "../static/seed_images/kit_1/snowstorm_painting.jpg"}, {'name': "valentine_pup", 'image_url': "../static/seed_images/kit_1/valentine_pup.jpg"}, {'name': "Marshmallow Snowman", 'image_url': "../static/seed_images/kit_1/marshmallow_snowman.jpg"}]
        product = Product.add_product("February Kit 21", 5.00, "../static/seed_images/kit_1/product_image.jpg", "not_selling", subproducts)

        # add an order including one purchase row for two kits
        purchases = [{'product_id': product.id, 'number_ordered': 2, 'number_made': 0}]
        order = Order.add_order("fakestripeid", "First", "Last", datetime.datetime.now(), "fake@gmail.com", "received", "", purchases)

    def tearDown(self):
        db.session.rollback()


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

    def test_order_edit(self):
        # test editing the order
        o = Order.query.filter_by(stripe_order_id = "fakestripeid").first()
        purchases = o.purchases
        for purchase in purchases:
            purchase.name = "Edited Name"
        o.edit_order(o.stripe_order_id, "Editfirst", "Editlast", datetime.datetime.now(), "editfake@gmail.com", "packaged", "ship it to this address: 1234 potus, washington", purchases)
        self.assertEqual(o.first_name, "Editfirst")
        self.assertEqual(o.last_name, "Editlast")
        self.assertEqual(type(o.date_time), datetime.datetime)
        self.assertEqual(o.email, "editfake@gmail.com")
        self.assertEqual(o.status, "packaged")
        self.assertEqual(o.notes, "ship it to this address: 1234 potus, washington")
        self.assertEqual(o.purchases[0].name, "Edited Name")


    def test_order_delete(self):
        # test deleting the order which should delete any attatched purchases
        o = Order.query.filter_by(stripe_order_id = "fakestripeid").first()
        delete = o.delete_order()
        self.assertEqual(delete, True)
        all_purchases = Purchase.query.all()
        self.assertEqual(len(all_purchases), 0)


class PurchaseModelTestCase(TestCase):
    def setUp(self):
         # delete and create tables
        db.drop_all()
        db.create_all()
        
        # add a product row and subproducts for that product
        subproducts = [{'name': "Punxsutawney Phil", 'image_url': "../static/seed_images/kit_1/punxsutawney_phil.jpg"}, {'name': "Snowstorm Painting", 'image_url': "../static/seed_images/kit_1/snowstorm_painting.jpg"}, {'name': "valentine_pup", 'image_url': "../static/seed_images/kit_1/valentine_pup.jpg"}, {'name': "Marshmallow Snowman", 'image_url': "../static/seed_images/kit_1/marshmallow_snowman.jpg"}]
        product = Product.add_product("February Kit 21", 5.00, "../static/seed_images/kit_1/product_image.jpg", "not_selling", subproducts)

        # add an order including one purchase row for two kits
        purchases = [{'product_id': product.id, 'number_ordered': 2, 'number_made': 0}]
        order = Order.add_order("fakestripeid", "First", "Last", datetime.datetime.now(), "fake@gmail.com", "received", "", purchases)

    def tearDown(self):
        db.session.rollback()

    def test_purchase_row(self):
        # test the row for an added purchase
        prod = Product.query.filter_by(name = "February Kit 21").first()
        p = Purchase.query.filter_by(product_id = prod.id).first()
        self.assertEqual(type(p.order_id), int)
        self.assertEqual(p.product_id, prod.id)
        self.assertEqual(p.number_ordered, 2)
        self.assertEqual(p.number_made, 0)
        self.assertEqual(p.order.first_name, "First")

    def test_purchase_edit(self):
        # test editing a purchase
        prod = Product.query.filter_by(name = "February Kit 21").first()
        p = Purchase.query.filter_by(product_id = prod.id).first()
        p.edit_purchase(p.order_id, p.product_id, p.number_ordered, 2)
        self.assertEqual(p.number_made, 2)

    def test_product_purchases_relationships(self):
        # test the relationships between a purchase and its product that is being purchased
        prod = Product.query.filter_by(name = "February Kit 21").first()
        purchases = prod.purchases
        self.assertEqual(len(purchases), 1)
        product = purchases[0].product
        self.assertEqual(product, prod)


