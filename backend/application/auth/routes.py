from flask import jsonify
from flask_login import login_user

from application import db
from application.models import Users
from flask_restful import Resource

from config import Config
from . import api_auth
from .fields_validation import register_data, register_validation, login_data, login_validation
from ..auth.auth import create_token, register_main_admin


class Register(Resource):
    def post(self):
        data = register_data.parse_args()
        register_validation(data)
        user = Users(email=data['email'], role='user')
        db.session.add(user)
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
        user = Users.query.filter_by(email=data['email']).first()
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
