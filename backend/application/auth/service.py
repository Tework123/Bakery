from application import db
from application.models import User, Order


def get_user(email):
    user = User.query.filter_by(email=email).first()
    return user


def create_user(email, code):
    user = User(email=email, role='user', code=code)
    db.session.add(user)
    user = User.query.filter_by(email=email).first()
    basket = Order(user_id=user.user_id)
    db.session.add(basket)
    db.session.commit()
