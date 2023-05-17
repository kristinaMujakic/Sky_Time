'''Flask app for Sky Time'''

import os

from flask import Flask, g, session, render_template, redirect, flash, jsonify, request
import requests
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError


from forms import SignUpForm, LogInForm
from models import db, connect_db, User, Location, UserFavourite

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///sky_time'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "333")

toolbar = DebugToolbarExtension(app)

# Read the API key from the file
with open('api_key.txt', 'r') as file:
    API_KEY = file.read().strip()

# Set the API key as an environment variable
os.environ['API_KEY'] = API_KEY
ASTRONOMY_API_URL = f'https://api.ipgeolocation.io/astronomy?apiKey={API_KEY}'

with app.app_context():
    connect_db(app)
    db.create_all()


@app.before_request
def user_global():
    '''If the User is logged in, add to Flask global'''

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def user_login(user):
    '''Login the User'''

    session[CURR_USER_KEY] = user.username


def user_logout():
    '''Logout the User'''

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def homepage():
    '''Render homepage'''

    if g.user:
        return render_template('user.html')

    else:
        return render_template('homepage.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    '''Handle User signup'''

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(username=form.username.data,
                               email=form.email.data, image_url=form.image_url.data or User.image_url.default.arg, password=form.password.data)

            db.session.commit()

        except IntegrityError:
            flash('The username you fancy has already been occupied by another lucky soul! Please specify an alternate. \:) ', 'danger')

            return render_template('signup.html', form=form)

        user_login(user)

        return redirect('/')

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Handle User login'''

    form = LogInForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            user_login(user)
            flash(
                f"Welcome, {user.username} the sky explorer! Enjoy the cosmic ride!", 'success')
            return redirect('/')

        flash('Your credentials seem to be playing hide-and-seek with authenticity. No luck this time, my friend! Let\'s give it another shot, shall we?', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    '''Handle User logout'''

    user_logout()

    flash(
        f"Goodbye, Sky Explorer! Safe travels through the celestial expanse until we meet again!", 'success')

    return redirect('/login')


@app.route('/search', methods=['POST'])
def user_page():
    '''Handle search form submission'''

    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect('/')

    data = request.get_json()

    try:
        response = requests.get(ASTRONOMY_API_URL, params=data)
        astronomical_data = response.json()

        location = astronomical_data['location']
        date = astronomical_data['date']
        sunrise = astronomical_data['sunrise']
        sunset = astronomical_data['sunset']
        day_length = astronomical_data['day_length']
        moonrise = astronomical_data['moonrise']
        moonset = astronomical_data['moonset']

        search_data = Location(
            city=location['city'],
            state=location['state'],
            country=location['country'],
            date=date,
            latitude=location['latitude'],
            longitude=location['longitude']
        )

        db.session.add(search_data)
        db.session.commit()

        response = {
            "location": location,
            "date": date,
            "sunrise": sunrise,
            "sunset": sunset,
            "day_length": day_length,
            "moonrise": moonrise,
            "moonset": moonset
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error retrieving location data: {str(e)}")
        flash('An error occurred while retrieving location data. Please try again later.', 'danger')
        return redirect('/')
