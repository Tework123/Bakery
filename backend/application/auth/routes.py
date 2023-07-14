from flask import jsonify
from flask_login import login_user, current_user

from application import db
from application.models import User, Order
from flask_restful import Resource

from config import Config
from . import api_auth
from .fields_validation import register_data, register_validation, login_data, login_validation
from ..auth.auth import create_token, register_main_admin, verify_token
from ..email.email import send_email_authentication


class Register(Resource):

    def get(self, token):
        # я могу сам этот рендер темплейт отправить
        # нужно отправлять ссылку, на нее тыкают и токен приходит сюда, варифицируется и происходит добавление в базу
        # а потом и автоматический логин, с логином тоже надо почту сделать
        email = verify_token(token)
        print(token)
        response = jsonify({'data': 'Токен пришел'})
        response.status_code = 200
        return response

    def post(self):
        data = register_data.parse_args()
        register_validation(data)

        token = create_token(data['email'], 500)
        send_email_authentication(data['email'], token)

        user = User(email=data['email'], role='user')
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        user = User.query.filter_by(email=data['email']).first()
        basket = Order(user_id=user.user_id)
        db.session.add(basket)
        db.session.flush()
        db.session.commit()
        response = jsonify({'data': 'Регистрация прошла успешно'})
        response.status_code = 200
        return response


class Login(Resource):
    def post(self):
        data = login_data.parse_args()

        # проверка на главного админа
        if data['email'] == Config.MAIN_ADMIN_EMAIL:
            register_main_admin(data['email'])
            response = jsonify({'data': 'Вход главного админа выполнен успешно'})
            response.status_code = 200
            return response

        login_validation(data)
        user = User.query.filter_by(email=data['email']).first()
        user.token = create_token(data['email'])
        db.session.commit()
        login_user(user)
        if user.role == 'admin':
            response = jsonify({'data': 'Вход админа выполнен успешно'})
        else:
            response = jsonify({'data': 'Вход выполнен успешно'})
        response.status_code = 200
        return response


api_auth.add_resource(Login, '/login')
api_auth.add_resource(Register, '/register')
