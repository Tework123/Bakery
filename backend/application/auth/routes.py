import datetime
import random

from flask import jsonify, session, request, make_response
from flask_login import login_user, current_user, logout_user

from application import db
from application.models import User, Order
from flask_restful import Resource

from config import Config
from . import api_auth
from .fields_validation import register_validation, login_data, login_validation, token_data, \
    token_login_data, login_email_data, login_email_validation, login_email_code_data, login_email_code_validation
from ..auth.auth import create_token, verify_token, register, login_required, send, create_code, \
    example_users_validation

from ..email.email import send_email_authentication, send_email_register


def login_user_remember(user, verified=False):
    login_user(user, remember=True, duration=datetime.timedelta(days=180))
    user.verified = verified
    db.session.commit()


class LoginEmail(Resource):
    def post(self):
        data = login_email_data.parse_args()
        login_email_validation(data)
        email = data['email']

        # проверка на тестовых пользователей
        response_from_register = example_users_validation(email)
        if response_from_register:
            response = jsonify({'data': response_from_register})
            response.status_code = 200
            return response

        user = User.query.filter_by(email=email).first()
        code = create_code()

        # если такой email есть, то проверяются куки, если они есть, то вход допущен
        if user:
            user.code = code
            db.session.commit()

            # если кук нет, то аккаунт verified = False, устанавливаются куки, и отправляется код на почту для
            # подтверждения
            if not current_user.is_authenticated:
                login_user_remember(user, verified=False)
                send_email_authentication(data['email'], code)
                response = jsonify({'data': 'Код для авторизации отправлен вам на почту'})
                response.status_code = 200
                return response

            # если пользователь с куками одного аккаунта переходит в другой
            if current_user.email != user.email:
                login_user_remember(user, verified=False)
                send_email_authentication(data['email'], code)
                response = jsonify({'data': 'Код для авторизации отправлен вам на почту'})
                response.status_code = 200
                return response

            # если аккаунт verified = False, но куки есть, то отправляется код на почту для подтверждения
            if not user.verified:
                send_email_authentication(data['email'], code)
                response = jsonify({'data': 'У вас уже есть аккаунт, но его нужно подтвердить.'
                                            ' Код для подтверждения регистрации отправлен вам на почту'})
                response.status_code = 200
                return response

            response = jsonify({
                'data': 'Вы вошли в аккаунт'})
            response.status_code = 200
            return response

        # если пользователя нет в базе, то он создается, аккаунт нужно активировать, для этого отправляется код
        user = User(email=email, role='user', code=code)
        db.session.add(user)
        user = User.query.filter_by(email=email).first()
        basket = Order(user_id=user.user_id)
        db.session.add(basket)
        db.session.flush()
        db.session.commit()

        # при указании email сразу происходит вход в аккаунт, но он не активирован
        login_user_remember(user, verified=False)

        # отправка кода на email
        send_email_authentication(data['email'], code)

        response = jsonify({'data': 'Код для подтверждения регистрации отправлен вам на почту'})
        response.status_code = 200
        return response


class LoginPhone(Resource):
    pass


class LoginEmailCode(Resource):
    def post(self):
        data = login_email_code_data.parse_args()
        login_email_code_validation(data)

        code = int(data['code'])

        if not current_user.is_authenticated:
            response = jsonify({'data': 'Вы не вошли в аккаунт'})
            response.status_code = 403
            return response

        if current_user.code != code:
            response = jsonify({'data': 'Код неверный'})
            response.status_code = 403
            return response

        current_user.verified = True
        db.session.commit()

        response = jsonify({'data': 'Аккаунт подтвержден'})
        response.status_code = 200
        return response


# LEGACY

#
# class RegisterPhone(Resource):
#     def post(self):
#         data = register_data.parse_args()
#         # register_validation(data)
#         email = data['email']
#         # token = create_token(data['email'], 500)
#         send(to=data['email'], msg='1234')
#         # отправка токена на email
#         # send_email_register(data['email'], token)
#
#         # отправка сообщения на номер телефона
#
#         response = jsonify({'data': 'Ссылка для подтверждения регистрации отправлена вам на почту'})
#         response.status_code = 200
#         return response
#
# #
# class Register(Resource):
#
#     def post(self):
#         data = register_data.parse_args()
#         register_validation(data)
#         email = data['email']
#         token = create_token(data['email'], 500)
#
#         # отправка токена на email
#         send_email_register(data['email'], token)
#
#         response = jsonify({'data': 'Ссылка для подтверждения регистрации отправлена вам на почту'})
#         response.status_code = 200
#         return response


class TokenRegister(Resource):
    def post(self):
        data = token_data.parse_args()

        try:
            email = verify_token(data['token'])
        except:
            response = jsonify({'data': 'Время действия ссылки истекло'})
            response.status_code = 200
            return response

        # можно один коммит сделать
        if email:
            user = User(email=email, role='user')
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            user = User.query.filter_by(email=email).first()
            basket = Order(user_id=user.user_id)
            db.session.add(basket)
            db.session.flush()
            db.session.commit()
            # при регистрации сразу происходит вход в аккаунт
            login_user(user, remember=True, duration=datetime.timedelta(days=180))

            response = jsonify({'data': 'Регистрация прошла успешно, можете сделать заказ', 'user_id': user.user_id})
            response.status_code = 200
            return response

        response = jsonify({'data': 'Что-то пошло не так, попробуйте зарегистрироваться еще раз'})
        response.status_code = 200
        return response


class Login(Resource):

    def post(self):
        data = login_data.parse_args()

        # проверка на тестового главного админа, тестового работника, тестового пользователя
        if data['email'] in [Config.MAIN_ADMIN_EMAIL, "restaurant@mail.ru", "user@mail.ru"]:

            if data['email'] == Config.MAIN_ADMIN_EMAIL:
                role = 'main_admin'
            elif data['email'] == "restaurant@mail.ru":
                role = 'restaurant'
            else:
                role = 'user'

            response_from_register = register(data['email'], role)
            response = jsonify({'data': response_from_register})
            response.status_code = 200
            return response

        login_validation(data)
        user = User.query.filter_by(email=data['email']).first()
        if user:
            token = create_token(data['email'], 500)
            send_email_authentication(data['email'], token)

            response = jsonify({'data': 'Ссылка для подтверждения входа отправлена вам на почту'})
            response.status_code = 200
            return response

        response = jsonify({'data': 'Вы еще не зарегистрированы'})
        response.status_code = 401
        return response


class TokenLogin(Resource):
    def post(self):
        data = token_login_data.parse_args()

        try:
            email = verify_token(data['token'])
        except:
            response = jsonify({'data': 'Время действия ссылки истекло'})
            response.status_code = 200
            return response

        if email:
            user = User.query.filter_by(email=email).first()
            login_user(user, remember=True, duration=datetime.timedelta(days=180))

            if user.role == 'restaurant':
                response = jsonify({'data': 'Вход админа выполнен успешно'})
            else:
                response = jsonify({'data': 'Вход выполнен успешно'})
            response.status_code = 200
            return response
        else:
            response = jsonify({'data': 'Что-то пошло не так, попробуйте войти еще раз'})
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
        response.status_code = 200
        return response


# api_auth.add_resource(Login, '/login')
# api_auth.add_resource(TokenLogin, '/token_login')
# api_auth.add_resource(RegisterPhone, '/register')
# api_auth.add_resource(TokenRegister, '/token_register')
api_auth.add_resource(Logout, '/logout')
api_auth.add_resource(LoginEmail, '/login')
api_auth.add_resource(LoginEmailCode, '/login_code')
