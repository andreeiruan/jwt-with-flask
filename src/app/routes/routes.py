from app import app
from flask import jsonify
from ..controllers import users, session
from ..middlewares.auth import token_required


@app.route('/', methods=['GET'])
@token_required
def root(current_user):
  return jsonify({'message': 'Hello World!', 'data': current_user.username})


@app.route('/users', methods=['POST'])
def post_user():
  return users.store()


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
  return users.update(id)


@app.route('/users', methods=['GET'])
def get_users():
  return users.index()


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
  return users.show(id)


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
  return users.delete(id)


@app.route('/session',methods=['POST'])
def login():
  return session.authenticate()