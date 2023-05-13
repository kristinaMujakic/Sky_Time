'''Models for Sky Time app'''

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def connect_db(app):
    '''Connect database to Flask app'''
    with app.app_context():
        db.app = app
        db.init_app(app)
