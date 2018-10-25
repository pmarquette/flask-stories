from flask import render_template, flash, redirect, url_for, request
from app import app
from app.auth import blueprint
from app.auth.forms import LoginForm, RegistrationForm, PasswordResetForm, PasswordResetConfirmForm
from app.models import User, Post
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
import datetime
from app.auth.email import reset_password_email


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    new_user = User(email=form.email.data, username=form.username.data)
    new_user.set_password(form.password.data)
    new_user.save()
    flash('Registration successful')
    return redirect(url_for('auth.login'))
  return render_template('auth/register.html', title='Register', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.objects(username=form.username.data).first()
    if user is None or not user.check_password(password=form.password.data): 
      flash('Invalid username or password')
      return redirect(url_for('auth.login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)
  return render_template('auth/login.html', title='Sign In', form=form)


@blueprint.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))


@blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = PasswordResetForm()
  if form.validate_on_submit():
    user = User.objects(email=form.email.data).first()
    if user:
      reset_password_email(user)
      flash('Password reset email sent')
    return redirect(url_for('auth.login'))
  return render_template('auth/reset_password.html', title='Password Reset', form=form)


@blueprint.route('/reset_password_final/<token>', methods=['GET', 'POST'])
def reset_password_final(token):
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  user = User.verify_token(token)
  if not user:
    return redirect(url_for('index'))
  form = PasswordResetConfirmForm()
  if form.validate_on_submit():
    User.objects(username=user.username).update_one(set__password_hash = User.return_pw_hash(form.password.data))
    flash('Password changed')
    return redirect(url_for('login'))
  return render_template('auth/reset_password_final.html', title='Password Reset', form=form)