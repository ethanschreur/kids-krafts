"""Initializes the flask app."""
from flask import Flask, render_template, redirect, session, request
from forms import LoginForm
from models import connect_db, Product, db
from config import app_config
import os

app = Flask(__name__, static_folder='../static',)

def create_app(config_name):
    app.config.from_object(app_config[config_name])
    connect_db(app)
    return app

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """Produce login form or handle login or instant login."""
    if ("seller_email" in session):
        return redirect('/dashboard')
    form = LoginForm()
    if (form.validate_on_submit()):
        email = form.email.data
        pwd = form.password.data
        check_email = email.lower().strip() == os.environ.get('seller_email')
        check_password = pwd.lower().strip() == os.environ.get('seller_password')
        if (check_email and check_password):
            session['seller_email'] = os.environ.get('seller_email')
            return redirect('/dashboard')
    return render_template('seller/login.html', form = form)

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard', methods=['GET'])
def get_dashboard():
    if ("seller_email" not in session):
        return redirect('/login')
    return render_template('seller/dashboard.html') 

@app.route('/products', methods=['GET'])
def products():
    if ("seller_email" not in session):
        return redirect('/login')
    products = Product.query.all()
    print(products)
    return render_template('seller/products.html', products=products)

@app.route('/products', methods=['POST'])
def add_product():
    if ("seller_email" not in session):
        return redirect('/login')
    print(request.form)
    new_product = Product(
        name=request.form['product_name'],
        price=float(request.form['product_price']),
        image_url=request.form['product_image'],
        category=request.form["product_selling_status"])
    db.session.add(new_product)
    db.session.commit()
    return redirect('/products') 