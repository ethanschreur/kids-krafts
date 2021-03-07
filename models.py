from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)


class Seller(db.Model):
    __tablename__ = "sellers"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.Text, nullable = False, unique = True)
    password = db.Column(db.Text, nullable = False)

    # class methods
    @classmethod 
    def register(cls, email, pwd):
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        seller = cls(email = email, password = hashed_utf8)
        try:
            db.session.add(seller)
            db.session.commit()
            return seller
        except:
            return False
    
    @classmethod
    def authenticate(cls, email, pwd):
        u = cls.query.filter_by(email = email).first()
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False

    # instance methods
    def edit_seller(self, email, pwd):
        self.email = email
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        self.password = hashed_utf8
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False)
    price = db.Column(db.Float, nullable = False)
    image_url = db.Column(db.Text, nullable = False)
    category = db.Column(db.Text, nullable = False)

    # relationships
    purchases = db.relationship('Purchase', backref = "product", cascade = "all, delete-orphan")
    subproducts = db.relationship('Subproduct', backref = "product", cascade = "all, delete-orphan")

    # class methods
    @classmethod
    def add_product(cls, name, price, image_url, category, subproducts):
        product = cls(name = name, price = price, image_url = image_url, category = category)
        try:
            db.session.add(product)
            db.session.commit()
            if (len(subproducts) != 0):
                for sub in subproducts:
                    Subproduct.add_subproduct(product_id = product.id, name = sub["name"], image_url = sub["image_url"])
            return product
        except:
            return False

    # instance methods
    def edit_product(self, name, price, image_url, category, subproducts):
        self.name = name
        self.price = price
        self.image_url = image_url
        self.category = category
        try:
            db.session.add(self)
            db.session.commit()
            if (len(subproducts) != 0):
                for sub in subproducts:
                    sub.edit_subproduct(sub.product_id, sub.name, sub.image_url)
            return self
        except:
            return False
        
    def delete_product(self):
        if self.purchases:
            return False
        else:
            try:
                db.session.delete(self)
                db.session.commit()
                return True
            except:
                return False



class Subproduct(db.Model):
    __tablename__ = "subproducts"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable = False)
    name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False)

    # class methods
    @classmethod 
    def add_subproduct(cls, product_id, name, image_url):
        subproduct = cls(product_id = product_id, name = name, image_url = image_url)
        try:
            db.session.add(subproduct)
            db.session.commit()
            return subproduct
        except:
            return False

    # instance methods
    def edit_subproduct(self, product_id, name, image_url):
        self.product_id = product_id
        self.name = name
        self.image_url = image_url
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def delete_subproduct(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    stripe_order_id = db.Column(db.Text, nullable = False, unique = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    date_time = db.Column(db.DateTime, nullable = False)
    email = db.Column(db.Text, nullable = False)
    status = db.Column(db.Text, nullable = False)
    notes = db.Column(db.Text, nullable = False, default = "None")

    # relationships
    purchases = db.relationship('Purchase', backref = "order", cascade = "all, delete-orphan")
    
    # class methods
    @classmethod
    def add_order(cls, stripe_order_id, first_name, last_name, date_time, email, status, notes, purchases):
        order = cls(stripe_order_id = stripe_order_id, first_name = first_name, last_name = last_name, date_time = date_time, email = email, status = status, notes = notes)
        try:
            db.session.add(order)
            db.session.commit()
            if (len(purchases) != 0):
                for purchase in purchases:
                    Purchase.add_purchase(order_id = order.id, product_id = purchase['product_id'], number_ordered=purchase['number_ordered'], number_made = purchase['number_made'])
            return order
        except:
            return False
    
    # instance methods
    def edit_order(self, stripe_order_id, first_name, last_name, date_time, email, status, notes, purchases):
        self.stripe_order_id = stripe_order_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_time = date_time
        self.email = email
        self.status = status
        self.notes = notes
        try:
            db.session.add(self)
            db.session.commit()
            if (len(purchases) != 0):
                for purchase in purchases:
                    purchase.edit_purchase(purchase.order_id, purchase.product_id, purchase.number_ordered, purchase.number_made)
            return self
        except:
            return False
        
    def delete_order(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False


class Purchase(db.Model):
    __tablename__ = "purchases"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"),  nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable = False)
    number_ordered = db.Column(db.Integer, nullable = False)
    number_made = db.Column(db.Integer, nullable = False, default = 0)

    # class methods
    @classmethod 
    def add_purchase(cls, order_id, product_id, number_ordered, number_made):
        purchase = cls(order_id = order_id, product_id = product_id, number_ordered = number_ordered, number_made = number_made)
        try:
            db.session.add(purchase)
            db.session.commit()
            return purchase
        except:
            return False

    # instance methods
    def edit_purchase(self, order_id, product_id, number_ordered, number_made):
        self.order_id = order_id
        self.product_id = product_id
        self.number_ordered = number_ordered
        self.number_made = number_made
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False