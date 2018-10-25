from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for
from app import login, app
import jwt
from time import time

class User(UserMixin, Document):
  email = StringField(required=True)
  username = StringField(max_length=50)
  password_hash = StringField(max_length=128)
  profile_description = StringField(max_length=140)
  last_logon = DateTimeField()

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  @staticmethod
  def return_pw_hash(password):
    return generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def get_gravatar(self, pmarquette):
    if pmarquette:
      return 'https://en.gravatar.com/avatar/d25a5084ad0d9915fe001c0a3ee70ad5?s=128.'
    return 'https://en.gravatar.com/avatar/e8ec06ae7d4f42303e9f165830ab0f0c?s=128.'
  
  def get_reset_token(self):
    return jwt.encode({'reset_password': self.username, 'exp':time() + 500}, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

  @staticmethod
  def verify_token(token):
    try:
      username = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
    except:
      return
    return User.objects(username=username).first()

  # JSON for REST
  def to_dict(self):
    data = {
      'username': self.username,
      'email': self.email,
      'last_logon': self.last_logon,
      'profile_description': self.profile_description,
      'follower_count': len(FollowHelpers.return_followers(self)),
      'following_count': len(FollowHelpers.return_following(self)),
      '_links': {
        'account': url_for('user', username=self.username)
      }
    }
    return data
    
  def from_dict(self, data, new_user=False):
    for field in ['username', 'email', 'profile_description']:
      if field in data:
        setattr(self, field, data[field])
      if new_user and 'password' in data:
        self.set_password(data['password'])



@login.user_loader
def load_user(user_id):
  return User.objects(pk=user_id).first()


class Post(Document):
  body = StringField(max_length=140)
  timestamp = DateTimeField()
  user_fkey = ReferenceField(User)

  # JSON for REST
  def to_dict(self):
    data = {
      'username': self.user_fkey.username,
      'body': self.body,
      'timestamp': self.timestamp,
      '_links': {
        'post_creator': url_for('user', username=self.user_fkey.username)
      }
    }
    return data
    
  def from_dict(self, data):
    for field in ['username', 'body', 'timestamp']:
      if field in data:
        setattr(self, field, data[field])


class Follow(Document):
  follower_fkey = ReferenceField(User)
  following_fkey = ReferenceField(User)

  def follow(self, user):
    self.follower_fkey = self
    self.following_fkey = user


class FollowHelpers():
  @staticmethod
  def unfollow(current_user, followed_user):
    if FollowHelpers.is_following(current_user, followed_user):
      entry = Follow.objects(Q(following_fkey=followed_user) & Q(follower_fkey=current_user)).first()
      entry.delete()

  @staticmethod
  def is_following(current_user, followed_user):
    entry = Follow.objects(Q(following_fkey=followed_user) & Q(follower_fkey=current_user)).first() # followerkey=Jackie
    if entry:
      return True
    return False

  @staticmethod
  def return_following(current_user):
    following_list = []
    for following in Follow.objects(follower_fkey=current_user):
      following_list.append(following)
    return following_list
  
  @staticmethod
  def return_followers(current_user):
    followers_list = []
    for following in Follow.objects(following_fkey=current_user):
      followers_list.append(following)
    return followers_list

  @staticmethod
  def return_following_posts(current_user):
    posts_list = []
    following_list = FollowHelpers.return_following(current_user)
    for following in following_list:
      individual_posts = []
      for posts in Post.objects(user_fkey=following.following_fkey):
        individual_posts.append(posts)
      for individual_post in individual_posts:
        posts_list.append(individual_post)
    posts_list.sort(key=lambda x: x.timestamp, reverse=True)
    return posts_list