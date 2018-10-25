from app import app
from app.api import blueprint
from app.models import Post
from flask import jsonify, url_for, request

@blueprint.route('/posts/<string:id>', methods=['GET'])
def get_post(id):
  return jsonify(Post.objects(pk=id).first().to_dict())

@blueprint.route('/posts', methods=['Post'])
def make_post():
  data = request.get_json() or {}
  # incomplete data
  if 'username' not in data or 'body' not in data or 'timestamp' not in data:
    return
  post = Post()
  post.from_dict(data)
  post.save()
  response = jsonify(post.to_dict())
  response.status_code = 201
  return response