from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User


class EditProfileForm(FlaskForm):
  profile_description = TextAreaField('Profile description', validators=[Length(min=0, max=140)])
  submit = SubmitField('Submit')


class PostForm(FlaskForm):
  post = TextAreaField('Say something', validators=[
    DataRequired(),Length(min=1, max=140)])
  submit = SubmitField('Submit')