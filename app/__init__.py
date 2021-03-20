"""Initializes the flask app."""
from flask import Flask, render_template, redirect, session
from models import connect_db
from config import app_config

app = Flask(__name__)

def create_app(config_name):
    app.config.from_object(app_config[config_name])
    connect_db(app)
    return app

@app.route('/products', methods=['GET', 'POST'])
def products():
    """View and post products"""
    if ("seller_email" in session):
        return redirect('/dashboard')
    return render_template('seller/products.html')