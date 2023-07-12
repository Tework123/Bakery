from flask import Blueprint
from flask_restful import Api

bp = Blueprint('auth', __name__)
api_auth = Api(bp)

from . import routes
