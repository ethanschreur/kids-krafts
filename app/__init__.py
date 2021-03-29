"""Initializes the flask app."""
from flask import Flask, render_template, redirect, session
from forms import LoginForm
from models import connect_db
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