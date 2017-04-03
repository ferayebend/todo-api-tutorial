from flask import jsonify, make_response
from . import api

def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

@api.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'not found'}), 404)
