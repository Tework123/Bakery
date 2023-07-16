from flask import jsonify
from flask_login import login_user, current_user

from application import db
from application.models import User, Order
from flask_restful import Resource

from config import Config
from . import api_auth
from .fields_validation import register_data, register_validation, login_data, login_validation
from ..auth.auth import create_token, register_main_admin, verify_token
from ..email.email import send_email_authentication, send_email_register


class Register(Resource):
    # как то наладить, чтобы мое письмо пересылало на url сайта, а там его ловил фронт и куки появлялись
    # понятно, что postman не видит, ведь этот url через него не проходи и функция login_user не срабатывает
    # если после этого снова через postman работать, видимо, только через браузер
    # ограничение от gmail в 100 писем в день, хаххах, переходим на телефон, а это пока для теста
    def get(self, token):
        try:
            email = verify_token(token)
        except:
            response = jsonify({'data': 'Время действия ссылки истекло'})
            response.status_code = 200
            return response

        if email:
            user = User(email=email, role='user')
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            user = User.query.filter_by(email=email).first()
            basket = Order(user_id=user.user_id)
            user.token = create_token(email, 86400 * 180)
            db.session.add(basket)
            db.session.flush()
            db.session.commit()

            # при регистрации сразу происходит вход в аккаунт
            login_user(user)
            response = jsonify({'data': 'Регистрация прошла успешно, можете сделать заказ'})
            response.status_code = 200
            return response

        response = jsonify({'data': 'Что-то пошло не так, попробуйте зарегистрироваться еще раз'})
        response.status_code = 200
        return response

    def post(self):
        data = register_data.parse_args()
        register_validation(data)

        token = create_token(data['email'], 500)
        send_email_register(data['email'], token)

        response = jsonify({'data': 'Ссылка для подтверждения регистрации отправлена вам на почту'})
        response.status_code = 200
        return response


class Login(Resource):
    def get(self, token):
        email = verify_token(token)
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

    def post(self):
        print(current_user)

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


api_auth.add_resource(Login, '/login', '/login/<string:token>')
api_auth.add_resource(Register, '/register', '/register/<string:token>')
