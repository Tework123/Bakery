from flask import Blueprint
from flask_restful import Api

bp = Blueprint('email', __name__, template_folder='templates')
api_email = Api(bp)

from . import email