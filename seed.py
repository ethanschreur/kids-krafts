from models import db, connect_db
from app import app

with app.app_context():
    connect_db(app)
    db.drop_all()
    db.create_all()