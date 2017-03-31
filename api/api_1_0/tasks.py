from flask import jsonify, request, abort, url_for
from . import api
from .. import db
from ..models import Task


@api.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = [task.to_json() for task in Task.query.all()] # TODO add pagination
    return jsonify({'tasks':tasks})

@api.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_json())

@api.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = Task.from_json(request.json)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_json()), 201, \
           {'Location': url_for('api.get_task', task_id=task.id, _external=True)}

@api.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task.title = request.json.get('title', task.title)
    task.description = request.json.get('description', task.description)
    task.done = request.json.get('done', task.done)
    db.session.commit()
    return jsonify(task.to_json()), 201, \
           {'Location': url_for('api.get_task', task_id=task.id, _external=True)}

@api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task_id = task.id
    db.session.delete(task)
    db.session.commit()
    return jsonify({'deleted': task_id}), 201