from flask import Blueprint
from flask_restful import Api

bp = Blueprint('admin', __name__)
api_admin = Api(bp)

from . import routes
