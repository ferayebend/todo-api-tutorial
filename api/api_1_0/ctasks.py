from flask import Blueprint, g, url_for, abort, jsonify
from .errors import not_found
from .. import celery

ctasks_bp = Blueprint('ctasks', __name__)


@celery.task
def run_flask_request(environ):
    #import app
    pass

@ctasks_bp.route('/status/<id>', methods=['GET'])
def get_status(id):
    """
    Return status about an asynchronous task. If this request returns a 202
    status code, it means that task hasn't finished yet. Else, the response
    from the task is returned.
    task = run_flask_request.AsyncResult(id)
    if task.state == states.PENDING:
        abort(404)
    if task.state == states.RECEIVED or task.state == states.STARTED:
        return '', 202, {'Location': url_for('tasks.get_status', id=id)}
    return task.info
    """
    return jsonify({}), 202, {'Location': url_for('ctasks.get_status', id=id)}
