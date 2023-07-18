from flask import jsonify, request, session
from flask_login import current_user
from flask_restful import Resource, Api

from config import DevelopmentConfig
from config import ProductionConfig

from application import create_app

CONFIG = ProductionConfig

app = create_app(CONFIG)
