from flask import render_template
from . import main

@main.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
