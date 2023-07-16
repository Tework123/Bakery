from flask import Blueprint
from flask_restful import Api

bp = Blueprint('basket', __name__)
api_basket = Api(bp)

from . import routes
