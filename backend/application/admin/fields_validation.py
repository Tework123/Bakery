import re

from werkzeug.datastructures import FileStorage
from flask_restful import reqparse, abort

from application.models import User

# создание админа
create_admin_data = reqparse.RequestParser()
create_admin_data.add_argument('email', type=str, help='Требуется email для регистрации админа', required=True)


# create_user_data.add_argument('phone', type=str, help='Требуется телефон для регистрации', required=True)


def create_admin_validation(data):
    # может сделать вывод сразу всех ошибок через этот словарик, после проверки каждого поля.
    errors = {}
    if User.query.filter_by(email=data['email']).first():
        abort(400, message='Данный email уже занят')
    if '@' not in data['email'] or '.' not in data['email']:
        abort(400, message='Email записан некорректно')
    # if Users.query.filter_by(phone=data['phone']).first():
    #     abort(400, message='Данный номер телефона уже занят')
    # if not bool(re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
    #                      data['phone'])):
    #     abort(400, message='Номер телефона записан некорректно')


# удаление админа
delete_admin_data = reqparse.RequestParser()
delete_admin_data.add_argument('email', type=str, help='Требуется email для удаления админа', required=True)
