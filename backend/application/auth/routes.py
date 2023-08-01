import datetime
import time
from flask import jsonify
from flask_login import login_user, current_user, logout_user
from application import db
from application.models import User, Order
from flask_restful import Resource
from . import api_auth
from .fields_validation import login_email_data, login_email_validation, login_email_code_data, \
    login_email_code_validation
from ..auth.auth import create_code, example_users_validation
from ..email.email import send_email_authentication, celery_task_send_email_authentication


class LoginEmail(Resource):
    def post(self):
        if current_user.is_authenticated:
            response = jsonify({'data': 'Вы уже вошли в аккаунт'})
            response.status_code = 200
            return response

        data = login_email_data.parse_args()
        login_email_validation(data)
        email = data['email']

        # проверка на тестовых пользователей
        response_from_register = example_users_validation(email)
        if response_from_register:
            response = jsonify({'data': response_from_register})
            response.set_cookie('remember_token2', current_user.role, max_age=86400 * 365)
            response.status_code = 200
            return response

        user = User.query.filter_by(email=email).first()
        code = create_code()

        # если есть такой email в базе, но куков нет, то отправляется код на email
        if user:
            user.code = code
            db.session.commit()

            # отправка кода на email

            send_email_authentication(data['email'], code)
            celery_task_send_email_authentication(data['email'], code)

            response = jsonify({'data': 'Код для авторизации отправлен на почту'})
            response.status_code = 200
            return response

        # если такого email нет, то он добавляется в базу, отправляется код
        user = User(email=email, role='user', code=code)
        db.session.add(user)
        user = User.query.filter_by(email=email).first()
        basket = Order(user_id=user.user_id)
        db.session.add(basket)
        db.session.commit()
        send_email_authentication(data['email'], code)
        celery_task_send_email_authentication(data['email'], code)

        response = jsonify({'data': 'Для подтверждения регистрации введите код из почты'})
        response.status_code = 200
        return response


class LoginEmailCode(Resource):
    def post(self):
        if current_user.is_authenticated:
            response = jsonify({'data': 'Вы уже вошли в аккаунт'})
            response.status_code = 200
            return response

        data = login_email_code_data.parse_args()
        login_email_code_validation(data)

        code = int(data['code'])
        user = User.query.filter_by(email=data['email']).first()

        if user.code != code:
            response = jsonify({'data': 'Код неверный'})
            response.status_code = 403
            return response

        login_user(user, remember=True, duration=datetime.timedelta(days=365))

        response = jsonify({'data': 'Аккаунт подтвержден'})
        response.set_cookie('remember_token2', User.role, max_age=86400 * 365)
        response.status_code = 200
        return response


class Logout(Resource):
    def get(self):
        if not current_user.is_authenticated:
            response = jsonify({'data': 'Вы не зашли в аккаунт'})
            response.status_code = 200
            return response

        logout_user()
        response = jsonify({'data': 'Вы вышли из аккаунта'})
        response.set_cookie('remember_token2', '', max_age=0)

        response.status_code = 200
        return response


api_auth.add_resource(Logout, '/logout')
api_auth.add_resource(LoginEmail, '/login')
api_auth.add_resource(LoginEmailCode, '/login_code')
