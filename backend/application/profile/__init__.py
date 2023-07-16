from flask import Blueprint
from flask_restful import Api

bp = Blueprint('profile', __name__)
api_profile = Api(bp)

from . import routes
