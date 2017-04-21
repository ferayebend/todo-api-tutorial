from flask import Blueprint
from .auth import auth

api = Blueprint('api',__name__)

@api.before_request
@auth.login_required
def before_request():
    pass

from . import tasks, users, errors
from ..tasks import run_flask_request # does not do anything but import necessary?
