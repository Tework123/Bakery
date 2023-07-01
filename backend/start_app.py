from flask import redirect, url_for

from config import DevelopmentConfig

from application import create_app

CONFIG = DevelopmentConfig
CONFIG_TEST = ''

app = create_app(CONFIG)


@app.route('/')
def index():
    return redirect(url_for('main.index'))
