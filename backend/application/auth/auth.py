import dataclasses
import datetime
import logging
import random
import re
from time import time

import requests
from flask import jsonify
import jwt
from flask_login import login_user

from application import db
from application.models import User, Order
from config import Config

log = logging.getLogger("SMS")


def send(to: str, msg: str):
    url = 'https://sms.ru/sms/send'
    api_id = '158E35A1-337C-2CB8-D9FA-95FEB998BF1A'
    to = to
    msg = msg
    response = requests.get(url, params=dict(
        api_id=api_id,
        to=to,
        msg=msg,
        json=1
    )).json()

    log.debug("Response %s", response)
    print(response)

    if response["status"] == "OK":
        phone = response["sms"][to]

        if phone["status"] == "OK":
            return jsonify(
                {"status": 1,
                 "status_code": phone["status_code"],
                 "balance": response['balance'],
                 "id": phone["sms_id"]}
            )

    log.debug("Error status %s", response)
    return jsonify({
        "status_code": response["status_code"]}
    )


def login_required(user):
    def wrap(func):
        def wrapper(*args, **kwargs):
            if not user.is_authenticated:
                response = jsonify({'data': 'Вы не зашли в аккаунт'})
                response.status_code = 401
                return response
            if not user.verified:
                response = jsonify({'data': 'Ваш аккаунт не подтвержден'})
                response.status_code = 403
                return response

            return func(*args, **kwargs)

        return wrapper

    return wrap


def restaurant_login_required(user):
    def wrap(func):
        def wrapper(*args, **kwargs):
            if not user.is_authenticated:
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
            if not user.is_authenticated:
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


def example_users_validation(email):
    if email in [Config.MAIN_ADMIN_EMAIL, "restaurant@mail.ru", "user@mail.ru"]:

        if email == Config.MAIN_ADMIN_EMAIL:
            role = 'main_admin'
        elif email == "restaurant@mail.ru":
            role = 'restaurant'
        else:
            role = 'user'

        response_from_register = register(email, role)
        return response_from_register
    else:
        return False


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
        user.verified = True
        db.session.commit()
        return register_response

    user = User(email=email, role=role, verified=True)
    db.session.add(user)
    user = User.query.filter_by(email=email).first()
    basket = Order(user_id=user.user_id)
    db.session.add(basket)
    db.session.flush()
    db.session.commit()
    login_user(user, remember=True, duration=datetime.timedelta(days=180))
    return register_response


def create_code():
    code = ''
    for i in range(4):
        code += str(random.randrange(0, 10))
    print(code)
    return code


def create_token(email, exp=600):
    token = jwt.encode({'email': email, 'exp': int(time()) + exp}, Config.SECRET_KEY,
                       algorithm='HS256')
    return token


def verify_token(token):
    email = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])['email']

    return email
