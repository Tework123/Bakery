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


# для фронта: когда он тыкает на отправить email, то делается post запрос на login, и логин возвращает email
# этот email показывается рядом с полем ввода кода, когда код вводится - емайл и код летят на другую url


# Сделать так, чел вводит свой емайл, нажимает на - отправить код.
# Он добавляется в базу, но куки не даются. Verified также False.
# Появляется окно, где уже написан емайл,
# и требуется ввести код. Когда вводит, все улетает на новый url. По этому емайлу он достается, пароли сверяются
# Даются куки и verified True

# Если у чела просрочились куки, то он вводит свой емайл, как ниже короче будет, только он введет код.

# Если рандомный чел вводит не свой емайл, то в базе находится этот емайл, так как кук нет, то нужно входить
# отправляется код на емайл. Чтобы получить доступ нужен код.
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


api_auth.add_resource(Logout, '/logout')
api_auth.add_resource(LoginEmail, '/login')
api_auth.add_resource(LoginEmailCode, '/login_code')
