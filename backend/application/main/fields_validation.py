import re

from flask_restful import reqparse, abort

from application.models import Users

register_data = reqparse.RequestParser()
register_data.add_argument('name', type=str, help='Требуется имя для регистрации', required=True)
register_data.add_argument('email', type=str, help='Требуется email для регистрации', required=True)
register_data.add_argument('password', type=str, help='Требуется пароль для регистрации', required=True)
register_data.add_argument('phone', type=str, help='Требуется телефон для регистрации', required=True)


def register_validation(data):
    # может сделать вывод сразу всех ошибок через этот словарик, после проверки каждого поля.
    errors = {}
    if Users.query.filter_by(email=data['email']).first():
        abort(400, message='Данный email уже занят')
    if '@' not in data['email'] or '.' not in data['email']:
        abort(400, message='Email записан некорректно')
    if not 4 < len(data['password']) < 25 or not any(map(str.isdigit, data['password'])):
        abort(400, message='Пароль должен иметь длину от 5 до 24 символов и содержать цифры')
    if Users.query.filter_by(phone=data['phone']).first():
        abort(400, message='Данный номер телефона уже занят')
    if not bool(re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
                         data['phone'])):
        abort(400, message='Номер телефона записан некорректно')


login_data = reqparse.RequestParser()
login_data.add_argument('email', type=str, help='email for login required', required=True)
login_data.add_argument('password', type=str, help='password for login required', required=True)


def login_validation(data):
    user = Users.query.filter_by(email=data['email']).first()
    if not user:
        abort(403, message='Данный email не зарегистрирован')
    if user.password != data['password']:
        abort(403, message='Пароль неверный')


card_data = reqparse.RequestParser()
card_data.add_argument('name', type=str, help='name for card required', required=True)
card_data.add_argument('price', type=int, help='price for card required', required=True)
