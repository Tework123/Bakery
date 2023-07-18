import datetime
import random

from flask import jsonify, session, request, make_response
from flask_login import login_user, current_user

from application import db
from application.models import User, Order
from flask_restful import Resource

from config import Config
from . import api_auth
from .fields_validation import register_data, register_validation, login_data, login_validation, token_data, \
    token_login_data, code_data
from ..auth.auth import create_token, register_main_admin, verify_token
from ..email.email import send_email_authentication, send_email_register


class Register(Resource):

    def post(self):
        data = register_data.parse_args()
        register_validation(data)
        email = data['email']
        token = create_token(data['email'], 500)
        # token = ''
        # for i in range(4):
        #     digit = random.randrange(0, 9)
        #     token += str(digit)
        send_email_register(data['email'], token)

        # if email:
        #     user = User(email=email, role='user')
        #     db.session.add(user)
        #     db.session.flush()
        #     db.session.commit()
        #     user = User.query.filter_by(email=email).first()
        #     basket = Order(user_id=user.user_id)
        #     user.token = create_token(email, 86400 * 180)
        #     db.session.add(basket)
        #     db.session.flush()
        #     db.session.commit()

        # при регистрации сразу происходит вход в аккаунт
        # login_user(user)
        #     login_user(user, remember=True, duration=datetime.timedelta(days=30))
        #     # login_user(user)
        # response = jsonify({'data': 'Вы зарегистрированы'})

        response = jsonify({'data': 'Ссылка для подтверждения регистрации отправлена вам на почту'})
        response.status_code = 200
        return response


class TokenRegister(Resource):
    def post(self):
        data = token_data.parse_args()
        print(data)

        try:
            email = verify_token(data['token'])
        except:
            response = jsonify({'data': 'Время действия ссылки истекло'})
            response.status_code = 200
            return response

        print(email)
        print(email)

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
            login_user(user, remember=True, duration=datetime.timedelta(days=30))

            response = jsonify({'data': 'Регистрация прошла успешно, можете сделать заказ', 'user_id': user.user_id})
            response.status_code = 200
            return response

        response = jsonify({'data': 'Что-то пошло не так, попробуйте зарегистрироваться еще раз'})
        response.status_code = 200
        return response


class Login(Resource):

    def post(self):
        print(current_user)
        print('********************88888*******88*****')
        print('********************88888*******88*****')
        print('********************88888*******88*****')

        data = login_data.parse_args()

        # проверка на главного админа
        if data['email'] == Config.MAIN_ADMIN_EMAIL:
            register_main_admin(data['email'])
            response = jsonify({'data': 'Вход главного админа выполнен успешно'})
            response.status_code = 200
            return response

        login_validation(data)
        user = User.query.filter_by(email=data['email']).first()
        if user:
            # отправка на email ссылки
            # user.token = create_token(data['email'], 86400 * 180)
            # db.session.commit()
            # login_user(user)
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

            user.token = create_token(email, 86400 * 180)
            db.session.commit()
            login_user(user)
            if user.role == 'admin':
                response = jsonify({'data': 'Вход админа выполнен успешно'})
            else:
                response = jsonify({'data': 'Вход выполнен успешно'})
            response.status_code = 200
            return response
        else:
            response = jsonify({'data': 'Что-то пошло не так, попробуйте войти еще раз'})
            response.status_code = 200
            return response


class Code(Resource):
    def post(self):
        data = code_data.parse_args()
        print(data)
        response = jsonify({'data': f'Ваш код найден: {data}'})
        response.status_code = 200
        return response


api_auth.add_resource(Login, '/login')
api_auth.add_resource(TokenLogin, '/token_login')
api_auth.add_resource(Register, '/register')
api_auth.add_resource(TokenRegister, '/token_register')
api_auth.add_resource(Code, '/code')
