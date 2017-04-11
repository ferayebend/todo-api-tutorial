from flask import jsonify, url_for, current_app

def unauthorized(message=None):
    if message is None:
        if current_app.config['USE_TOKEN_AUTH']:
            message = 'Please authenticate with your token.'
        else:
            message = 'Please authenticate.'
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': message})
    response.status_code = 401
    if current_app.config['USE_TOKEN_AUTH']:
        response.headers['Location'] = url_for('token.request_token')
    return response

def not_found(message):
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': message})
    response.status_code = 404
    return response


def not_allowed():
    response = jsonify({'status': 405, 'error': 'method not allowed'})
    response.status_code = 405
    return response

