from application import db
from application.models import User


def get_all_restaurant():
    restaurants = User.query.filter_by(role='restaurant').all()
    return restaurants


def create_restaurant(email):
    user = User(email=email, role='restaurant')
    db.session.add(user)
    db.session.commit()


def delete_restaurant(email):
    User.query.filter_by(email=email).delete()
    db.session.commit()
