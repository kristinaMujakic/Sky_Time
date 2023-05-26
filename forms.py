'''Forms for Sky Time app'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class SignUpForm(FlaskForm):
    '''Form for a user to sign up'''

    username = StringField('Username', validators=[
                           DataRequired()], render_kw={'placeholder': 'Username'})
    email = StringField(
        'E-mail', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', validators=[
                             Length(min=6)], render_kw={'placeholder': 'Password'})
    image_url = StringField('(Optional) Image URL',
                            render_kw={'placeholder': 'URL image'})


class LogInForm(FlaskForm):
    '''Form for a user to login'''

    username = StringField('Username', validators=[
                           DataRequired()], render_kw={'placeholder': 'Username'})
    password = PasswordField('Password', validators=[
                             Length(min=8)], render_kw={'placeholder': 'Password'})
