"""Initializes the flask app."""
from flask import Flask, render_template, redirect, session, request, flash, jsonify, url_for
from forms import LoginForm, ContactForm
from models import connect_db, Product, db, Subproduct, Order, Purchase
from config import app_config
from .helper import get_two_weeks_options, whichOption, get_last_week, get_first_week, get_new_first_week, get_new_last_week, get_next_month, get_prev_month, get_first_month, get_second_month, get_month_header
from .filters import filter_products, filter_orders, search_orders
import os
from flask_mail import Message, Mail
import random
import calendar
import datetime
import stripe

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
    if 'order_by' in request.args:
        print('here')
        products = filter_products(request.args['order_by'], request.args['value'], products)
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
    images_file.close()
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
    if 'cart' not in session:
        session['cart'] = {}
    if 'total' not in session:
        session['total'] = 0
    if(request.args.get('shipping') == 'true' and session['cart'] != {} and session['total'] != 0):
        order = []
        for id in session['cart']:
            prod = []
            prod.append(session['cart'][id]['name'])
            prod.append(session['cart'][id]['amount'])
            order.append(prod)
        form.message.data = f"""Order: {str(order)[1:-1]}
Total: ${session['total']} (before shipping)
Shipping Address:
Notes:"""
        form.subject.data = "Shipping Request"
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
        total = total + (float(session['cart'][id]['price']) * float(session['cart'][id]['amount']))
    session['total'] = round(total, 2)
    return render_template('/customer/cart.html', order_details=True)

@app.route('/cart', methods=['POST'])
def add_to_cart():
    rows = session['cart']
    rows[str(request.json['id'])] = {'name': request.json['name'], 'image': request.json['image'], 'price': request.json['price'], 'amount': 1}
    session['cart'] = rows
    return redirect('/shop')

@app.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    id = request.json['id']
    cart = session['cart']
    del cart[f'{id}']
    session['cart'] = cart
    return redirect('/cart')

@app.route('/cart/amount', methods=['POST'])
def change_amount():
    id = request.json['id']
    amount = request.json['amount']
    cart = session['cart']
    cart[f"{id}"]['amount'] = amount
    session['cart']=cart
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

@app.route('/create-checkout-session', methods=['POST'])
def pay():
    pickup = request.json['pickup']
    month = request.json['month']
    session['datetime'] = month + ' ' + pickup
    items = []
    for id in session['cart']:
        items.append({
        'price_data': {
            'currency': 'usd',
            'product_data': {
            'name': session['cart'][id]['name'],
            },
            'unit_amount': round(float(session['cart'][id]['price'])*100),
        },
        'quantity': session['cart'][id]['amount'],
        });
    stripe.api_key = app.config['STRIPE_SECRET_KEY']
    stripe_session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=items,
    mode='payment',
    success_url = url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
    cancel_url = url_for('order_details', _external=True),
    )
    return jsonify(id=stripe_session.id)

@app.route('/success')
   # display order and pickup information, remove cart from session.
def success():
    try:
        stripe.api_key = app.config['STRIPE_SECRET_KEY']
        stripe_session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
        customer = stripe.Customer.retrieve(stripe_session.customer)
        name = stripe.PaymentIntent.retrieve(stripe_session.payment_intent).charges.data[0].billing_details.name;
        email = customer.email
        datetime = session['datetime']
        stripe_order_id = request.args.get('session_id')
        datetime = session['datetime']
        # add new order and purchases and clear cart
        new_order = Order(
            stripe_order_id=stripe_order_id,
            name=name,
            pickup_time = datetime,
            email = email,
            status = "ordered",
            payment_type="stripe",
            payment_status="paid",
            )
        db.session.add(new_order)
        db.session.commit()
        if 'cart' in session:
            for id in session['cart']:
                new_purchase = Purchase(order_id=new_order.id, product_id=id, number_ordered=session['cart'][id]['amount'], number_made=0)
                db.session.add(new_purchase)
                db.session.commit()
            del session['cart']
        session['total']=0
        parts = datetime.split(" ")
        day=parts[0] + ' ' + parts[1]
        time=''
        if (parts[2] == 'AM'):
            time="8 and 12 AM"
        else:
            time="12 and 6 PM"
        return render_template('/customer/success.html', email=email, name=name, day=day, time=time)
    except:
        return redirect('/shop')

@app.route('/orders', methods=['GET'])
def orders():
    if ("seller_email" not in session):
        return redirect('/login')
    orders = Order.query.all()
    if 'order_by' in request.args and 'value' in request.args:
        orders = filter_orders(request.args['order_by'], request.args['value'], orders)
    elif 'order_by' in request.args:
        orders = filter_orders(request.args['order_by'], '', orders)
    elif len(request.args) != 0:
        orders = search_orders(list(request.args.keys())[0], list(request.args.values())[0], orders)
    return render_template('seller/orders.html', orders=orders)

@app.route('/orders', methods=['POST'])
def add_order():
    if ("seller_email" not in session):
        return redirect('/login')
    notes = 'None'
    if (request.form['order_notes'] != ''):
        notes = request.form['order_notes']
    new_order = Order(
        stripe_order_id="none",
        name=request.form['order_name'],
        pickup_time=request.form['order_pickup_time'],
        email=request.form['order_email'],
        status="ordered",
        payment_type="not stripe",
        payment_status="not paid",
        notes=notes)
    db.session.add(new_order)
    db.session.commit()
    return redirect('/orders')

@app.route('/orders/<id>', methods=['GET'])
def get_order(id):
    if ("seller_email" not in session):
        return redirect('/login')
    order = Order.query.get_or_404(id)
    products = Product.query.all()
    prod_info = {}
    for prod in products:
        prod_info[prod.id] = [prod.name, prod.image_url]
    return render_template('seller/order.html', order = order, products=products, prod_info=prod_info)

@app.route('/orders/<id>', methods=['POST'])
def update_order(id):
    if ("seller_email" not in session):
        return redirect('/login')
    order = Order.query.get_or_404(id)
    order.stripe_order_id = request.form['order_stripe_order_id']
    order.name = request.form['order_name']
    order.pickup_time = request.form['order_pickup_time']
    order.email = request.form['order_email']
    order.status = request.form['order_status']
    order.payment_type = request.form['order_payment_type']
    order.payment_status = request.form['order_payment_status']
    order.notes = request.form['order_notes']
    db.session.add(order)
    db.session.commit()
    return redirect(f'/orders/{id}')

@app.route('/orders/<id>/delete', methods=['GET'])
def delete_order(id):
    if ("seller_email" not in session):
        return redirect('/login')
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()
    return redirect('/orders')

@app.route('/orders/<id>/purchases', methods=['POST'])
def add_purchase(id):
    if ("seller_email" not in session):
        return redirect('/login')
    new_purchase = Purchase(
        order_id = id,
        product_id = request.form['product_id'],
        number_ordered = request.form['number_ordered'],
        number_made = 0
    )
    db.session.add(new_purchase)
    db.session.commit()
    return redirect(f'/orders/{id}')

@app.route('/orders/<id>/purchases/<pid>', methods=['POST'])
def update_purchases(id, pid):
    if ("seller_email" not in session):
        return redirect('/login')
    purchase = Purchase.query.get(pid)
    purchase.number_ordered = request.form['number_ordered']
    purchase.number_made = request.form['number_made']
    db.session.add(purchase)
    db.session.commit()
    return redirect(f'/orders/{id}')

@app.route('/orders/<id>/purchases/<pid>/delete', methods=["GET"])
def delete_purchases(id, pid):
    if ('seller_email' not in session):
        return redirect('/login')
    purchase = Purchase.query.get(pid)
    db.session.delete(purchase)
    db.session.commit()
    return redirect(f'/orders/{id}')
