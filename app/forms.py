from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired
import json


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AdminPasswordResetForm(FlaskForm):
    username = SelectField('Select User', choices=[])  # Choices will be populated in the route
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
