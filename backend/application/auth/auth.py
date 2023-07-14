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


def create_token(email):
    token = jwt.encode({'email': email, 'exp': int(time()) + 1000}, Config.SECRET_KEY,
                       algorithm='HS256')
    return token
