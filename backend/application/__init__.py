from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from application.main import bp as bp_main
        app.register_blueprint(bp_main, url_prefix='/main')

        from application.admin import bp as bp_admin
        app.register_blueprint(bp_admin, url_prefix='/admin')

        db.drop_all()
        db.create_all()

    return app
