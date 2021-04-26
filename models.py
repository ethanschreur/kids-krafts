"""Creates the object relational manager for the database and sets up all the relationships between tables."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)
    db.create_all()


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


class Subproduct(db.Model):
    __tablename__ = "subproducts"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable = False)
    name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    stripe_order_id = db.Column(db.Text, nullable = False)
    name = db.Column(db.Text, nullable = False)
    pickup_time = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, nullable = False)
    status = db.Column(db.Text, nullable = False)
    payment_type = db.Column(db.Text, nullable=False)
    payment_status = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable = False, default="None")
    # relationships
    purchases = db.relationship('Purchase', backref = "order", cascade = "all, delete-orphan")


class Purchase(db.Model):
    __tablename__ = "purchases"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"),  nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable = False)
    number_ordered = db.Column(db.Integer, nullable = False)
    number_made = db.Column(db.Integer, nullable = False, default = 0)
