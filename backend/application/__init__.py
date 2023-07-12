from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config):
    app = Flask(__name__)
    cors = CORS(app, origins="*")

    app.config.from_object(config)
    app.json.sort_keys = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():

        from application.main import bp as bp_main
        app.register_blueprint(bp_main)

        from application.profile import bp as bp_profile
        app.register_blueprint(bp_profile, url_prefix='/profile')

        from application.admin import bp as bp_admin
        app.register_blueprint(bp_admin, url_prefix='/admin')

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
