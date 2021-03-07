from flask import Flask
from models import connect_db



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///kids-krafts'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
connect_db(app)
