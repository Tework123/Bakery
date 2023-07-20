import datetime
from time import time
from flask import jsonify
import jwt
from flask_login import login_user

from application import db
from application.models import User, Order
from config import Config


def login_required(user):
    def wrap(func):
        def wrapper(*args, **kwargs):
            try:
                user_id = user.user_id
                # походу можно без jwt токена здесь, чисто проверить через try except на наличие у юзера id например
                # если анонимус - то ошибка, и все, а в login зададим remember 180 дней
                # токен чисто на почту отправляется
            except:
                response = jsonify({'data': 'Вы не зашли в аккаунт'})
                response.status_code = 401
                return response

            return func(*args, **kwargs)

        return wrapper

    return wrap


def admin_login_required(user):
    def wrap(func):
        def wrapper(*args, **kwargs):
            try:
                user_id = user.user_id
            except:
                response = jsonify({'data': 'Вы не зашли в аккаунт'})
                response.status_code = 401
                return response

            if user.role != 'restaurant' and user.role != 'main_admin':
                response = jsonify({'data': 'Вы не работник пекарни'})
                response.status_code = 403
                return response

            return func(*args, **kwargs)

        return wrapper

    return wrap


def register_main_admin(email):
    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user, remember=True, duration=datetime.timedelta(days=180))
        return True
    user = User(email=email, role='main_admin')
    db.session.add(user)
    user = User.query.filter_by(email=email).first()
    basket = Order(user_id=user.user_id)
    db.session.add(basket)
    db.session.flush()
    db.session.commit()
    login_user(user, remember=True, duration=datetime.timedelta(days=180))
    return True


def register_restaurant(email):
    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user, remember=True, duration=datetime.timedelta(days=180))
        return True
    user = User(email=email, role='restaurant')
    db.session.add(user)
    user = User.query.filter_by(email=email).first()
    basket = Order(user_id=user.user_id)
    db.session.add(basket)
    db.session.flush()
    db.session.commit()
    login_user(user, remember=True, duration=datetime.timedelta(days=180))
    return True


def register_user(email):
    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user, remember=True, duration=datetime.timedelta(days=180))
        return True
    user = User(email=email, role='user')
    db.session.add(user)
    user = User.query.filter_by(email=email).first()
    basket = Order(user_id=user.user_id)
    db.session.add(basket)
    db.session.flush()
    db.session.commit()
    login_user(user, remember=True, duration=datetime.timedelta(days=180))
    return True


def create_token(email, exp=600):
    token = jwt.encode({'email': email, 'exp': int(time()) + exp}, Config.SECRET_KEY,
                       algorithm='HS256')
    return token


def verify_token(token):
    print(token)
    email = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])['email']

    return email
