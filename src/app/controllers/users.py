from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify
from ..models.users import User, user_schema, users_schema


def store():
  username = request.json['username']
  password = request.json['password']
  name = request.json['name']
  email = request.json['email']

  pass_hash = generate_password_hash(password)
  user = User(username, pass_hash, name, email)

  try:
    db.session.add(user)
    db.session.commit()
    result = user_schema.dump(user)
    return jsonify({'message': 'successfully registered', 'data': result}), 201
  except:
    return jsonify({'message': 'unable to create', 'data': {}}), 500


def update(id):
  username = request.json['username']
  password = request.json['password']
  name = request.json['name']
  email = request.json['email']

  user = User.query.get(id)  

  if not user:
    return jsonify({'message': "User don't exist", 'data': {}}), 404

  pass_hash = generate_password_hash(password)

  try:
    user.username = username
    user.password = pass_hash
    user.name = name
    user.email = email
    print(user.id)
        
    db.session.commit()
    
    result = user_schema.dump(user)    
    return jsonify({'message': 'successfully registered', 'data': result}), 202
  except:
    return jsonify({'message': 'unable to create', 'data': {}}), 500


def index():
  users = User.query.all()

  if users:
    result = users_schema.dump(users)
    return jsonify({'message': 'successfully fetched', 'data': result})
  
  return jsonify({'message': 'nothing found', 'data': {}})


def show(id):
  user = User.query.get(id)

  if user:
    result = user_schema.dump(user)
    return jsonify({'message': 'successfully fetched', 'data': result})
  
  return jsonify({'message': "user dont't exist", 'data': {}})


def delete(id):
  user = User.query.get(id)

  if user:
    try:
      db.session.delete(user)
      db.session.commit()

      return jsonify({'data': {}}), 204 
    except:
      return jsonify({'message': 'Unable to delete', 'data': {}}), 500
  return jsonify({'message': "User don't exist", 'data': {}}), 404


def user_by_username(username):
  try:
    return User.query.filter(User.username == username).one()
  except:
    return None 