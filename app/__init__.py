"""Initializes the flask app."""
from flask import Flask, render_template
from models import connect_db
from config import app_config

app = Flask(__name__)

def create_app(config_name):
    app.config.from_object(app_config[config_name])
    connect_db(app)
    return app

@app.route('/shop')
def get_shop():
    return render_template('customer/shop.html') 