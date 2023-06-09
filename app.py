import os

from flask import Flask, g, session, render_template, redirect, flash, jsonify, request
import requests
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import SignUpForm, LogInForm
from models import db, connect_db, User

CURR_USER_KEY = 'curr_user'
ASTRONOMY_API_URL = 'https://api.ipgeolocation.io/astronomy'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///sky_time'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "333")

toolbar = DebugToolbarExtension(app)

# Read the API key from the file
with open('api_key.txt', 'r') as file:
    API_KEY = file.read().strip()

with app.app_context():
    connect_db(app)
    db.create_all()


@app.before_request
def user_global():
    '''If the User is logged in, add to Flask global'''

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    #   Retrieve form input from session and update g.user object
        if 'form_input' in session:
            g.user.form_input = session['form_input']

            print('USER GLOBAL', g.user.form_input)

    else:
        g.user = None


def user_login(user):
    '''Login the User and retrieve form input values'''

    session[CURR_USER_KEY] = user.username
    # session['form_input'] = g.user.form_input

    # Retrieve form input values from the session
    city = session.get('city')
    country = session.get('country')

    # Store form input values in the user object
    user.city = city
    user.country = country

    user.form_input = {
        'city': city,
        'country': country
    }

    print('user', user.form_input)


def user_logout():
    '''Logout the User'''

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def homepage():
    '''Render homepage'''

    if g.user:
        # Retrieve the form input from the session
        form_input = g.user.form_input
        print('HOMEPAGE', form_input)

        # Pass the form input to the template
        return render_template('user.html', form_input=form_input)

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
                               email=form.email.data, password=form.password.data)

            # Store the form input in the user object during signup
            user_login(user)

            db.session.commit()

        except IntegrityError:
            flash('The username you fancy has already been occupied by another lucky soul! Please specify an alternate. :) ', 'error')
            return render_template('signup.html', form=form)

        user_login(user)
        return redirect('/')

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Handle User login'''

    form = LogInForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            user_login(user)
            return redirect('/')

        flash('Your credentials seem to be playing hide-and-seek with authenticity. No luck this time, my friend! Let\'s give it another shot, shall we?', 'error')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    '''Handle User logout'''

    user_logout()

    return render_template('logout.html')


@app.route('/search', methods=['POST'])
def user_page():
    '''Handle search form submission'''

    if not g.user:
        flash('Access unauthorized', 'error')
        return redirect('/')

    data = request.get_json()

    try:
        city = data['city']
        country = data['country']

        # Store the form input in the session
        session['city'] = city
        session['country'] = country

        # Update the form_input dictionary in the session
        session['form_input'] = {
            'city': city,
            'country': country
        }

        # Update the form_input attribute in the user object
        g.user.form_input = session['form_input']

        response = requests.get(ASTRONOMY_API_URL, params={
            'apiKey': API_KEY, 'location': f'{city}, {country}'})

        astronomical_data = response.json()

        location = astronomical_data['location']
        date = astronomical_data['date']
        sunrise = astronomical_data['sunrise']
        sunset = astronomical_data['sunset']
        day_length = astronomical_data['day_length']
        moonrise = astronomical_data['moonrise']
        moonset = astronomical_data['moonset']

        search_data = {
            "city": location['city'],
            "country": location['country'],
            "date": date,
            "latitude": location['latitude'],
            "longitude": location['longitude']
        }

        resp = {
            "location": location,
            "date": date,
            "sunrise": sunrise,
            "sunset": sunset,
            "day_length": day_length,
            "moonrise": moonrise,
            "moonset": moonset,
        }

        return jsonify(resp)

    except Exception as e:
        print(f"Error retrieving location data: {str(e)}")
        flash('An error occurred while retrieving location data. Please try again later.', 'error')
        return redirect('/')
