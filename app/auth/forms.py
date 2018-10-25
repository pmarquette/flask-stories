from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User


class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField(
    'Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')

  def validate_username(self, username):
    user = User.objects(username=username.data).first()
    if user is not None:
      raise ValidationError('Username already exists')

  def validate_email(self, email):
    user = User.objects(email=email.data).first()
    if user is not None:
      raise ValidationError('Email already in use')


class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')


class PasswordResetForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired()])
  submit = SubmitField('Request Passsword Reset')


class PasswordResetConfirmForm(FlaskForm):
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField(
      'Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Reset Password')