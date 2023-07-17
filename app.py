import os

from flask import Flask, g, session, render_template, redirect, flash, jsonify, request
import requests
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

from forms import SignUpForm, LogInForm
from models import db, connect_db, User, SearchData

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
                               email=form.email.data, password=form.password.data)

            db.session.add(user)
            db.session.commit()

            user_login(user)
            return redirect('/')

        except IntegrityError:
            flash('The username you fancy has already been occupied by another lucky soul! Please specify an alternate. :) ', 'error')

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Handle User login'''

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

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

        if g.user:
            search_data = SearchData(
                user_id=g.user.username, city=city, country=country)

            print('search', search_data)

            db.session.add(search_data)
            db.session.commit()

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


@app.route('/favourites')
def favourites():
    '''Display user's last 5 search data from the database'''

    if not g.user:
        flash('Access unauthorized', 'error')
        return redirect('/')

    user = User.query.get(g.user.username)
    if not user:
        flash('User not found', 'error')
        return redirect('/')

    search_data = SearchData.query.filter_by(
        user_id=user.username).order_by(desc(SearchData.id)).limit(5).all()

    return render_template('favourites.html', search_data=search_data)


@app.route('/get_selected_data', methods=['POST'])
def get_selected_data():
    '''Handle form submission for selected data'''

    if not g.user:
        flash('Access unauthorized', 'error')
        return redirect('/')

    data = request.get_json()

    try:
        selected_data = []

        for item in data:
            city = item['city']
            country = item['country']

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

            selected_data.append({
                'location': location,
                'date': date,
                'sunrise': sunrise,
                'sunset': sunset,
                'day_length': day_length,
                'moonrise': moonrise,
                'moonset': moonset
            })

        return jsonify(selected_data)

    except Exception as e:
        print(f"Error retrieving location data: {str(e)}")
        flash('An error occurred while retrieving location data. Please try again later.', 'error')
        return redirect('/')
