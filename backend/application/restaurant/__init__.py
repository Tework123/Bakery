from flask import Blueprint
from flask_restful import Api

bp = Blueprint('restaurant', __name__)
api_restaurant = Api(bp)

from . import routes
