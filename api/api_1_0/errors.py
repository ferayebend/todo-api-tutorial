from flask import jsonify, make_response
from . import api
from ..errors import not_allowed

def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

@api.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'not found'}), 404)

@api.app_errorhandler(405)
def method_not_allowed_error(error):
    return not_allowed()
