from flask import Blueprint, jsonify, g
from flask_httpauth import HTTPBasicAuth
from ..models import User
from ..errors import unauthorized

token = Blueprint('token', __name__)
token_auth = HTTPBasicAuth()

@token_auth.verify_password
def verify_password(name, password):
    g.user = User.query.filter_by(name=username).first()
    if not g.user:
        return False
    return g.user.verify_password(password)


@token_auth.error_handler
def unauthorized_error():
    return unauthorized('Please authenticate to get your token.')


@token.route('/request-token', methods=['POST'])
@token_auth.login_required
def request_token():
    # Note that a colon is appended to the token. When the token is sent in
    # the Authorization header this will put the token in the username field
    # and an empty string in the password field.
    return jsonify({'token': g.user.generate_auth_token() + ':'})
