'''Flask app for Sky Time'''

from flask import Flask
from models import db, connect_db


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sky_time'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '333'

with app.app_context():
    connect_db(app)
    db.create_all()
