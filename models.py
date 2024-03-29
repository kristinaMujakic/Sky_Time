from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    '''Connect database to Flask app'''
    with app.app_context():
        db.app = app
        db.init_app(app)


class User(db.Model):
    '''User in the system'''

    __tablename__ = 'users'

    username = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    search_data = db.relationship('SearchData', back_populates='user')

    locations = db.relationship(
        'Location', back_populates='user', cascade='all, delete')

    favourites = db.relationship(
        'UserFavourite', back_populates='user', cascade='all, delete')

    @classmethod
    def signup(cls, username, email, password):
        '''Sign up User: hashes password and adds user to the system'''

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, email=email,
                    password=hashed_pwd)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        '''Match the User with username and password'''

        user = cls.query.filter_by(username=username).first()

        if user:
            is_authenticated = bcrypt.check_password_hash(
                user.password, password)
            if is_authenticated:
                return user

        return False


class Location(db.Model):
    '''The astronomical information based on location'''

    __tablename__ = 'locations'

    location_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.username'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    date = db.Column(db.Date)

    user = db.relationship('User', back_populates='locations')
    favourites = db.relationship(
        'UserFavourite', back_populates='location', cascade='all, delete')


class UserFavourite(db.Model):
    '''Saving User's preferences'''

    __tablename__ = 'users_favourites'

    favourite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.username'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))
    date = db.Column(db.Date)
    sunrise_time = db.Column(db.Time)
    sunset_time = db.Column(db.Time)
    moonrise_time = db.Column(db.Time)
    moonset_time = db.Column(db.Time)
    day_length = db.Column(db.Time)

    user = db.relationship('User', back_populates='favourites')
    location = db.relationship('Location', back_populates='favourites')


class SearchData(db.Model):
    '''Model for storing search data'''

    __tablename__ = 'search_data'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.username'))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))

    user = db.relationship('User', back_populates='search_data')
