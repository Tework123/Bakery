import time

from flask import redirect, url_for, jsonify

from config import DevelopmentConfig
from config import ProductionConfig

from application import create_app

CONFIG = ProductionConfig
CONFIG_TEST = ''

app = create_app(CONFIG)


# @app.route('/time')
# def index():
#     return {'data': time.time()}
#
#
# @app.route('/time2')
# def admin():
#     return {'data': time.time()}

#     # return redirect(url_for('main.index'))
