from flask import Blueprint
from flask_restful import Api

bp = Blueprint('cards', __name__)
api_cards = Api(bp)

from . import routes
