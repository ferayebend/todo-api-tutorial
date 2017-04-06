from flask import jsonify, request, abort, url_for
from . import api
from .. import db
from ..models import User

@api.route('/users', methods=['GET'])
def get_users():
    users = [user.to_json() for user in User.query.all()] # TODO add pagination
    return jsonify({'users':users})

@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_json())

@api.route('/users', methods=['POST'])
def create_user():
    if not request.json or not 'name' in request.json:
        abort(400)
    user = User.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json()), 201, \
           {'Location': url_for('api.get_user', user_id=user.id, _external=True)}
'''
@api.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task.title = request.json.get('title', task.title)
    task.description = request.json.get('description', task.description)
    task.done = request.json.get('done', task.done)
    db.session.commit()
    return jsonify(task.to_json()), 201, \
           {'Location': url_for('api.get_task', task_id=task.id, _external=True)}
'''
@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    user_id = user.id
    db.session.delete(user)
    db.session.commit()
    return jsonify({'deleted': user_id}), 201
