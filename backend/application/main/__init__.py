from flask import Blueprint
from flask_restful import Api

bp = Blueprint('main', __name__)
api_main = Api(bp)

from . import routes
