import re

from flask_restful import reqparse, abort

from application.models import User

login_email_data = reqparse.RequestParser()
login_email_data.add_argument('email', type=str, help='Требуется email для регистрации', required=True)


# register_data.add_argument('phone', type=str, help='Требуется телефон для регистрации', required=True)
def login_email_validation(data):
    # if User.query.filter_by(email=data['email']).first():
    #     abort(400, message='Данный email уже занят')
    if '@' not in data['email'] or '.' not in data['email']:
        abort(400, message='Email записан некорректно')


login_email_code_data = reqparse.RequestParser()
login_email_code_data.add_argument('code', type=str, help='Требуется код из 4 цифр', required=True)


def login_email_code_validation(data):
    print(data)
    print(type(data))
    if len(data['code']) != 4:
        abort(400, message='Код должен содержать 4 цифры')
    if not data['code'].isdigit():
        abort(400, message='Код должен состоять только из цифр')


def register_validation(data):
    # может сделать вывод сразу всех ошибок через этот словарик, после проверки каждого поля.
    errors = {}
    # if User.query.filter_by(email=data['email']).first():
    #     abort(400, message='Данный email уже занят')
    # if '@' not in data['email'] or '.' not in data['email']:
    #     abort(400, message='Email записан некорректно')
    if User.query.filter_by(phone=data['phone']).first():
        abort(400, message='Данный номер телефона уже занят')
    if not bool(re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
                         data['phone'])):
        abort(400, message='Номер телефона записан некорректно')


login_data = reqparse.RequestParser()
login_data.add_argument('email', type=str, help='Требуется email для входа', required=True)


def login_validation(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        abort(403, message='Данный email не зарегистрирован')


token_data = reqparse.RequestParser()
token_data.add_argument('token', type=str, help='Требуется token', required=True)

token_login_data = reqparse.RequestParser()
token_login_data.add_argument('token', type=str, help='Требуется token', required=True)
