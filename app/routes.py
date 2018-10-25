from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import EditProfileForm, PostForm
from app.models import User, Post, Follow, FollowHelpers
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
import datetime
#from app.data_access_layer import DataAccess


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
  form = PostForm()
  cur_user = User.objects(username=current_user.username).first()
  if form.validate_on_submit():
    Post(body = form.post.data, user_fkey = cur_user, timestamp = datetime.datetime.now()).save()
    flash('Post successful')
    return redirect(url_for('index'))
  posts=[]
  for post in Post.objects(user_fkey=cur_user):
    posts.append(post)
  for post_other in FollowHelpers.return_following_posts(cur_user):
    posts.append(post_other)
  posts.sort(key=lambda x: x.timestamp, reverse=True)
  return render_template('index.html', title='Home', form=form, posts=posts)


@app.before_request
def before_request():
  if current_user.is_authenticated:
    User.objects(username=current_user.username).update_one(set__last_logon = datetime.datetime.now())


@app.route('/user/<username>')
@login_required
def user(username):
  user = User.objects(username=username).first()

  post_list = []
  for posts in Post.objects:
    post_list.append(posts)

  if user:
    return render_template('user.html', user=user, posts=post_list, FollowHelpers=FollowHelpers)
  flash('User does not exist')
  return redirect(url_for('index'))


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
  form = EditProfileForm()
  if form.validate_on_submit():
    User.objects(username=current_user.username).update_one(set__profile_description = form.profile_description.data)
    flash('Changes saved')
    return redirect(url_for('edit_profile'))
  elif request.method == 'GET':
    form.profile_description.data = current_user.profile_description
  return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
  user = User.objects(username=username).first()
  cur_user = User.objects(username=current_user.username).first()
  if user is None:
    flash('User {} not found.'.format(username))
    return redirect(url_for('index'))
  if user == current_user:
    flash('You cannot follow yourself')
    return redirect(url_for('index'))
  Follow(follower_fkey=cur_user, following_fkey=user).save()
  flash('You are following{} '.format(username))
  return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
  user = User.objects(username=username).first()
  cur_user = User.objects(username=current_user.username).first()
  if user is None:
    flash('User {} not found.'.format(username))
    return redirect(url_for('index'))
  if user == current_user:
    flash('You cannot unfollow yourself')
    return redirect(url_for('index'))
  FollowHelpers.unfollow(cur_user, user)
  flash('You are no longer following{} '.format(username))
  return redirect(url_for('user', username=username))


@app.route('/global_feed')
@login_required
def global_feed():
  all_posts = []
  for post in Post.objects:
    all_posts.append(post)
  all_posts.sort(key=lambda x: x.timestamp, reverse=True)
  return render_template('global_feed.html', title='Global Feed', posts=all_posts)


@app.route('/about')
def about():
  return render_template('about.html')