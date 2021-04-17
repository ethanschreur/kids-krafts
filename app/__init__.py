"""Initializes the flask app."""
from flask import Flask, render_template, redirect, session, request, flash
from forms import LoginForm, ContactForm
from models import connect_db, Product, db, Subproduct
from config import app_config
import os
import random
from flask_mail import Message, Mail

app = Flask(__name__, static_folder='../static',)

@app.template_filter('shuffle')
def filter_shuffle(seq):
    result = list(seq)
    random.shuffle(result)
    return result

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
    return render_template('seller/products.html', products=products)

@app.route('/products', methods=['POST'])
def add_product():
    if ("seller_email" not in session):
        return redirect('/login')
    new_product = Product(
        name=request.form['product_name'],
        price=float(request.form['product_price']),
        image_url=request.form['product_image'],
        category=request.form["product_selling_status"])
    db.session.add(new_product)
    db.session.commit()
    return redirect('/products')

@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    if ("seller_email" not in session):
        return redirect('/login')
    product = Product.query.get_or_404(id)
    return render_template('seller/product.html', prod = product)

@app.route('/products/<id>', methods=['POST'])
def update_product(id):
    if ("seller_email" not in session):
        return redirect('/login')
    product = Product.query.get_or_404(id)
    product.name = request.form['product_name']
    product.price = request.form['product_price']
    product.image_url = request.form['product_image']
    product.category = request.form['product_selling_status']
    db.session.add(product)
    db.session.commit()
    return redirect(f'/products/{id}')

@app.route('/products/<id>/delete', methods=['GET'])
def delete_product(id):
    if ("seller_email" not in session):
        return redirect('/login')
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/products')
    
@app.route('/products/<id>/subproducts', methods=['POST'])
def add_subproduct(id):
    if ("seller_email" not in session):
        return redirect('/login')
    new_subproduct = Subproduct(
        product_id = id,
        name = request.form['subproduct_name'],
        image_url = request.form['subproduct_image']
    )
    db.session.add(new_subproduct)
    db.session.commit()
    return redirect(f'/products/{id}')

@app.route('/products/<id>/subproducts/<sid>', methods=['POST'])
def update_subproducts(id, sid):
    if ("seller_email" not in session):
        return redirect('/login')
    subproduct = Subproduct.query.get(sid)
    subproduct.name = request.form['subproduct_name']
    subproduct.image_url = request.form['subproduct_image']
    db.session.add(subproduct)
    db.session.commit()
    return redirect(f'/products/{id}')

@app.route('/products/<id>/subproducts/<sid>/delete', methods=["GET"])
def delete_subproduct(id, sid):
    if ('seller_email' not in session):
        return redirect('/login')
    subproduct = Subproduct.query.get(sid)
    db.session.delete(subproduct)
    db.session.commit()
    return redirect(f'/products/{id}')

@app.route('/', methods=['GET'])
def landing_page():
    path = os.getcwd() + '/static/links.txt'
    images_file = open(path, 'r')
    images = images_file.readlines()
    return render_template('/customer/landing.html', images=images)

@app.route('/shop')
def shop_page():
    products = Product.query.all()
    return render_template('/customer/shop.html', products = products)

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    mail = Mail(app)
    form = ContactForm()
    if (form.validate_on_submit()):
        msg = Message(form.subject.data, sender='kidskrafts4u@gmail.com', recipients=[
            "%s" % (form.email.data)])
        msg.html = render_template('/customer/contact_email.html', email = "%s" % (form.email.data), name = "%s" % (form.name.data), message = "%s" % (form.message.data))
        mail.send(msg)
        flash('Your message was successfully sent')
        return redirect('/contact')
    return render_template('/customer/contact.html', form = form)