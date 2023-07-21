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
                # если анонимус - то ошибка, и все, а в login зададим remember 180 дней
                # токен на почту отправляется
            except:
                response = jsonify({'data': 'Вы не зашли в аккаунт'})
                response.status_code = 401
                return response

            return func(*args, **kwargs)

        return wrapper

    return wrap


def restaurant_login_required(user):
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


def admin_login_required(user):
    def wrap(func):
        def wrapper(*args, **kwargs):
            try:
                user_id = user.user_id
            except:
                response = jsonify({'data': 'Вы не зашли в аккаунт'})
                response.status_code = 401
                return response

            if user.role != 'main_admin':
                response = jsonify({'data': 'Вы не главный админ'})
                response.status_code = 403
                return response

            return func(*args, **kwargs)

        return wrapper

    return wrap


def register(email, role):
    user = User.query.filter_by(email=email).first()

    if role == 'main_admin':
        register_response = 'Вход тестового главного админа выполнен успешно'
    elif role == 'restaurant':
        register_response = 'Вход тестового работника выполнен успешно'
    else:
        register_response = 'Вход тестового пользователя выполнен успешно'

    if user:
        login_user(user, remember=True, duration=datetime.timedelta(days=180))
        return register_response

    user = User(email=email, role=role)
    db.session.add(user)
    user = User.query.filter_by(email=email).first()
    basket = Order(user_id=user.user_id)
    db.session.add(basket)
    db.session.flush()
    db.session.commit()
    login_user(user, remember=True, duration=datetime.timedelta(days=180))
    return register_response


def create_token(email, exp=600):
    token = jwt.encode({'email': email, 'exp': int(time()) + exp}, Config.SECRET_KEY,
                       algorithm='HS256')
    return token


def verify_token(token):
    email = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])['email']

    return email
