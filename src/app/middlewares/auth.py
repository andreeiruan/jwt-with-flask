from flask import request, jsonify
from functools import wraps
from app import app
from ..controllers.users import user_by_username
import jwt
import werkzeug.security

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.args.get('token')
    if not token:
      return jsonify({'message': 'token is missing', 'data': {}}), 401

    print(app.config['SECRET_KEY'])

    try:
      data = jwt.decode(token, app.config['SECRET_KEY'])
      current_user = user_by_username(username=data['username'])
    except:
      return jsonify({'message': 'token is invalid or expired', 'data': {}}), 401
    return f(current_user, *args, **kwargs)
  return decorated
      