from flask_login import current_user
from flask_restful import reqparse, abort
from application.models import User

profile_data = reqparse.RequestParser()
profile_data.add_argument('email', type=str, help='Требуется email', required=False)
profile_data.add_argument('address', type=str, help='Требуется address', required=False)


def email_validation(data):
    if data['email'] == current_user.email:
        abort(400, message='У вас уже установлен этот email')
    if User.query.filter_by(email=data['email']).first():
        abort(400, message='Данный email уже занят')
    if '@' not in data['email'] or '.' not in data['email']:
        abort(400, message='Email записан некорректно')
