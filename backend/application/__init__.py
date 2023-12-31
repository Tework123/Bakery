import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

from celery import Celery
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
celery = Celery(__name__, broker='redis://127.0.0.1:6379')


def create_app(config):
    app = Flask(__name__, static_folder='back_static')
    CORS(app, supports_credentials=True)

    app.config.from_object(config)

    app.json.sort_keys = False

    sentry_sdk.init(
        dsn=config.dsn, integrations=[FlaskIntegration(), ],
        environment=config.SENTRY_ENV,

        traces_sample_rate=1.0
    )

    celery.conf.update(app.config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    mail_handler = SMTPHandler(mailhost=(config.MAIL_SERVER, int(config.MAIL_PORT)),
                               fromaddr=config.MAIL_USERNAME,
                               toaddrs=config.ADMINS,
                               subject='Error from Bakery',
                               credentials=(config.MAIL_USERNAME, config.MAIL_PASSWORD),
                               secure=()
                               )
    # for SMTP logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/log_test.log', maxBytes=10240, backupCount=1)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

    # action to logs/log.log
    file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)

    # action to email
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    app.logger.setLevel(logging.ERROR)

    with app.app_context():
        from application.main import bp as bp_main
        app.register_blueprint(bp_main, url_prefix='/main')

        from application.email import bp as bp_email
        app.register_blueprint(bp_email, url_prefix='/email')

        from application.profile import bp as bp_profile
        app.register_blueprint(bp_profile, url_prefix='/profile')

        from application.admin import bp as bp_admin
        app.register_blueprint(bp_admin, url_prefix='/admin')

        from application.restaurant import bp as bp_restaurant
        app.register_blueprint(bp_restaurant, url_prefix='/restaurant')

        from application.auth import bp as bp_auth
        app.register_blueprint(bp_auth, url_prefix='/auth')

        from application.cards import bp as bp_cards
        app.register_blueprint(bp_cards, url_prefix='/cards')

        from application.basket import bp as bp_basket
        app.register_blueprint(bp_basket, url_prefix='/basket')

        # а здесь вложенные bluprints

        from application.command import bp as bp_command
        app.register_blueprint(bp_command)

    return app
