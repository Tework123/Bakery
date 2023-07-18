from time import time
from flask import jsonify
import jwt
from flask_login import login_user

from application import db
from application.models import User
from config import Config


def login_required(user):
    def wrap(func):
        def wrapper(*args, **kwargs):
            # try:
            if 1 == 1:
                if user.token:
                    # походу можно без jwt токена здесь, чисто проверить через try except на наличие у юзера id например
                    # если анонимус - то ошибка, и все, а в login зададим remember 180 дней
                    # токен чисто на почту отправляется
                    try:
                        data = jwt.decode(user.token, Config.SECRET_KEY, algorithms=['HS256'])

                    except:
                        response = jsonify({'data': 'Вы давно не заходили в свой аккаунт, попробуйте снова'})
                        response.status_code = 401
                        return response
            # except:
            else:
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
                if user.token:
                    try:
                        data = jwt.decode(user.token, Config.SECRET_KEY, algorithms=['HS256'])
                    except:
                        response = jsonify({'data': 'Вы давно не заходили в свой аккаунт, попробуйте снова'})
                        response.status_code = 401
                        return response
            except:
                response = jsonify({'data': 'Вы не зашли в аккаунт'})
                response.status_code = 401
                return response

            if user.role != 'admin' and user.role != 'main_admin':
                response = jsonify({'data': 'Вы не админ'})
                response.status_code = 403
                return response

            return func(*args, **kwargs)

        return wrapper

    return wrap


def register_main_admin(email):
    user = User.query.filter_by(email=email).first()
    if user:
        user.token = create_token(email)
        db.session.commit()
        login_user(user)
        return True
    user = User(email=email, role='main_admin')
    db.session.add(user)
    db.session.flush()
    db.session.commit()
    user = User.query.filter_by(email=email).first()
    user.token = create_token(email)
    db.session.commit()
    login_user(user)
    return True


def create_token(email, exp=600):
    token = jwt.encode({'email': email, 'exp': int(time()) + exp}, Config.SECRET_KEY,
                       algorithm='HS256')
    return token


def verify_token(token):
    token = token[1:]
    email = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])['email']

    return email
