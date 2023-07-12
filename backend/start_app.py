from flask import jsonify
from flask_restful import Resource, Api

from config import DevelopmentConfig
from config import ProductionConfig

from application import create_app

CONFIG = DevelopmentConfig

app = create_app(CONFIG)
