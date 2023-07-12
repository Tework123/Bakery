import os

from flask import jsonify, request
from flask_login import current_user
from flask_restful import Resource, fields, marshal_with

from application import db
from application.admin import api_admin
from application.admin.fields_validation import card_data, \
    card_patch_data, create_admin_data, create_admin_validation, delete_admin_data, card_delete_data
from application.auth.auth import admin_login_required
from application.models import CardProducts, Users
from config import Config
from start_app import CONFIG


# menu = [['Начальная страница', '/home'], ['О нас', '/we'], ['Войти', '/login']]
# если заходит админ, то показывается тот же сайт, как для юзера, но добавляется админ панелька в меню,
# там уже таблица с товарами и кнопочки

# нужно сделать все роуты в постман красиво со всеми ошибками, для документации
# нужно перенести это все в тестирование, о боже мой...
class Index(Resource):
    @admin_login_required(current_user)
    def get(self):
        response = jsonify({'data': 'admin panel here'})
        return response


class CreateAdmin(Resource):
    admins_fields = {
        'id_user': fields.Integer,
        'email': fields.String,
        'phone': fields.String,
        'role': fields.String
    }

    @admin_login_required(current_user)
    @marshal_with(admins_fields)
    def get(self):
        admins = Users.query.filter_by(role='admin').all()
        return admins

    @admin_login_required(current_user)
    def post(self):
        if current_user.email != Config.MAIN_ADMIN_EMAIL:
            response = jsonify({'data': 'Вы не являетесь главным админом'})
            response.status_code = 403
            return response

        data = create_admin_data.parse_args()
        create_admin_validation(data)
        user = Users(email=data['email'], role='admin')
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        response = jsonify({'data': 'Админ создан успешно'})
        response.status_code = 200
        return response

    @admin_login_required(current_user)
    def delete(self):
        if current_user.email != Config.MAIN_ADMIN_EMAIL:
            response = jsonify({'data': 'Вы не являетесь главным админом'})
            response.status_code = 403
            return response

        data = delete_admin_data.parse_args()
        Users.query.filter_by(email=data['email']).delete()
        db.session.commit()
        response = jsonify({'data': 'Админ удален успешно'})
        response.status_code = 403
        return response


class Cards(Resource):
    card_fields = {
        'card_id': fields.Integer,
        'card_name': fields.String,
        'card_price': fields.Price,
        'card_image': fields.String
    }

    @marshal_with(card_fields)
    def get(self):
        cards = CardProducts.query.all()
        # выводятся данные и на фронте расставляются в табличку с кнопками удалить, добавить
        return cards

    @admin_login_required(current_user)
    def post(self):
        data = card_data.parse_args()
        # file = request.files['card_image']
        print(data['card_image'][5:])

        # надо получить доступ к названию файла с .jpg и подставить его в путь к файлу, а то через id тяжко

        file_path = CONFIG.basepath + 'application/static/' + data['card_image']
        print(file_path)
        if not os.path.exists(file_path):
            data['card_image'].save(file_path)

        card = CardProducts(card_name=data['card_name'], card_price=data['card_price'])

        db.session.add(card)
        db.session.flush()
        db.session.commit()
        response = jsonify({'data': 'Товар добавлен успешно'})
        response.status_code = 200
        return response

    @admin_login_required(current_user)
    def delete(self):
        data = card_delete_data.parse_args()
        card = CardProducts.query.filter_by(card_id=data['card_id']).first()
        if card is None:
            response = jsonify({'data': 'Такого товара нет'})
            response.status_code = 200
            return response

        CardProducts.query.filter_by(card_id=data['card_id']).delete()
        db.session.commit()
        response = jsonify({'data': 'Товар удален успешно'})
        response.status_code = 200
        return response

    @admin_login_required(current_user)
    def patch(self):
        data = card_patch_data.parse_args()
        card = CardProducts.query.filter_by(card_id=data['card_id']).first()
        if card:
            change = ''
            for item, key in data.items():
                if item == 'card_id':
                    continue
                if key:
                    if item == 'card_name':
                        card.card_name = key
                    elif item == 'card_price':
                        card.card_price = key
                    elif item == 'card_image':
                        card.card_image = key
                    change += item

            db.session.commit()

            response = jsonify({'data': f'Следующие данные товара изменены: {change}'})
            response.status_code = 200
            return response
        else:
            response = jsonify({'data': 'Данный товар не найден'})
            response.status_code = 200
            return response


api_admin.add_resource(Index, '/')
api_admin.add_resource(Cards, '/cards')
api_admin.add_resource(CreateAdmin, '/create_admin')
