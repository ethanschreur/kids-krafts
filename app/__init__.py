"""Initializes the flask app."""
from flask import Flask, render_template, redirect, session, request, flash
from forms import LoginForm, ContactForm
from models import connect_db, Product, db, Subproduct
from config import app_config
from .helper import get_two_weeks_options, whichOption, get_last_week, get_first_week, get_new_first_week, get_new_last_week, get_next_month, get_prev_month, get_first_month, get_second_month, get_month_header
import os
from flask_mail import Message, Mail
import random
import calendar
import datetime

calendar.setfirstweekday(calendar.SUNDAY)

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
    if 'cart' not in session:
        session['cart'] = {}
    products = Product.query.all()
    return render_template('/customer/shop.html', products = products, shop=True)

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

@app.route('/about')
def about_page():
    return render_template('/customer/about.html')

@app.route('/cart', methods=['GET'])
def cart_page():
    if 'total' not in session:
        session['total'] = 0
    total = 0
    for id in session['cart']:
        total = total + float(session['cart'][id]['price'])
    session['total'] = total
    return render_template('/customer/cart.html', order_details=True)

@app.route('/cart', methods=['POST'])
def add_to_cart():
    rows = session['cart']
    rows[str(request.json['id'])] = {'name': request.json['name'], 'image': request.json['image'], 'price': request.json['price']}
    session['cart'] = rows
    return redirect('/shop')

@app.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    id = request.json['id']
    cart = session['cart']
    del cart[f'{id}']
    session['cart'] = cart
    return redirect('/cart')


@app.route('/order_details')
def order_details():
    month = int(datetime.datetime.now().strftime('%m'))
    year = int(datetime.datetime.now().strftime('%y'))
    two_weeks_options = get_two_weeks_options(month, year)
    today = datetime.datetime.now().day
    which = whichOption(today, two_weeks_options)
    last_week = get_last_week(which, two_weeks_options)
    first_week = get_first_week(which, two_weeks_options)
    last_week = get_new_last_week(last_week, which, two_weeks_options)
    first_week = get_new_first_week(first_week, which, two_weeks_options)

    prev_month = calendar.month_name[get_prev_month(month)]
    curr_month = calendar.month_name[month]
    next_month = calendar.month_name[get_next_month(month)]
    month_header = get_month_header(which, prev_month, curr_month, next_month, last_week, first_week)
    first_month = get_first_month(which, prev_month, curr_month)
    second_month = get_second_month(which, curr_month, next_month)
    return render_template('/customer/order_details.html', credit=True, month_header=month_header, first_month = first_month, second_month = second_month, last_week = last_week, first_week = first_week) 