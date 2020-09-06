from flask import request, jsonify
from functools import wraps
from datetime import datetime, timedelta
import jwt
from werkzeug.security import check_password_hash
from .users import user_by_username
from app import app


def authenticate():
  username = request.json['username']
  password = request.json['password']

  if not username or not password:
    return jsonify({'message': 'Could not verify',  'WWW-Authenticate': 'Basic auth="Login required"'}), 401

  user = user_by_username(username)
  if not user:
    return jsonify({'message': 'User not found', 'data': {}}), 404
  
  if user and check_password_hash(user.password, password):
    token = jwt.encode({'username': user.username, 'exp': datetime.now() + timedelta(hours=12)}, app.config['SECRET_KEY'])
    return jsonify({'message': 'Validated successufully', 'token': token.decode('UTF-8'),
                      'exp': datetime.now() + timedelta(hours=12)})
  
  return jsonify({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401
