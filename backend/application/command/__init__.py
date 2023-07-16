from flask import Blueprint

bp = Blueprint('command', __name__)

from application.command import routes
