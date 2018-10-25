from app import app
from app.api import blueprint
from app.models import User
from flask import jsonify, url_for, request


@blueprint.route('/users/<string:username>', methods=['GET'])
def get_user(username):
  return jsonify(User.objects(username = username).first().to_dict())

@blueprint.route('/users', methods=['POST'])
def create_user():
  data = request.get_json() or {}
  # incomplete data
  if 'username' not in data or 'email' not in data or 'password' not in data:
    return
  # user already exists
  if User.objects(username = data['username']).first():
    return
  # email already in use
  if User.objects(email = data['email']).first():
    return
  user = User()
  user.from_dict(data, new_user=True)
  user.save()
  response = jsonify(user.to_dict())
  response.status_code = 201
  response.headers['Location'] = url_for('api.get_user', username=user.username)
  return response