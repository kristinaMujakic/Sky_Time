'''Flask app for Sky Time'''

from flask import Flask, g, session, render_template, redirect, flash
from sqlalchemy.exc import IntegrityError

from forms import SignUpForm, LogInForm
from models import db, connect_db, User

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sky_time'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '333'

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
        return render_template('signup.html')


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
