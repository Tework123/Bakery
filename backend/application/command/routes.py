from flask.cli import with_appcontext
from application import db
from application.command import bp


@bp.cli.command('create_db')
@with_appcontext
def create_db():
    db.drop_all()
    db.create_all()
    print('create db')
    print('***Complete***')