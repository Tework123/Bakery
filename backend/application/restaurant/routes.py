import os

import sqlalchemy
from flask import jsonify, url_for
from flask_login import current_user
from flask_restful import Resource, fields, marshal_with
from sqlalchemy import or_, cast

from application import db
from application.auth.auth import restaurant_login_required
from application.models import CardProduct, Order, OrderProduct
from application.restaurant import api_restaurant
from application.restaurant.fields_validation import card_data, card_delete_data, card_patch_data, order_patch_data
from application.restaurant.helpers import pass_orders_to_list_dicts, current_orders_to_list_dicts
from application.restaurant.service import get_all_cards_product, add_card_product, delete_card_product, \
    get_card_product, get_pass_orders, get_current_orders
from start_app import CONFIG


class Index(Resource):
    def get(self):
        pass


class Cards(Resource):
    card_fields = {
        'card_id': fields.Integer,
        'name': fields.String,
        'price': fields.Integer,
        'image': fields.String
    }

    # здесь отправка картинок и всего остального для работников ресторана(тут с кнопками)
    @restaurant_login_required(current_user)
    @marshal_with(card_fields)
    def get(self):
        cards = get_all_cards_product()
        cards_dicts = []
        for row in cards:
            row = {'card_id': row.card_id, 'name': row.name, 'price': row.price,
                   'image': url_for('static', filename=row.image)}
            cards_dicts.append(row)

        # выводятся данные и на фронте расставляются в табличку с кнопками удалить, добавить
        return cards_dicts

    @restaurant_login_required(current_user)
    def post(self):

        data = card_data.parse_args()

        image = data['image']

        # сохранение полученной картинки
        file_path = CONFIG.basepath + 'application/static/' + image.filename

        if not os.path.exists(file_path):
            data['image'].save(file_path)

        try:
            add_card_product(data['name'], data['price'], image)
        except:
            db.session.rollback()
            response = jsonify({'data': 'Названия товара и картинки должны быть уникальными'})
            response.status_code = 400
            return response

        db.session.commit()
        response = jsonify({'data': 'Товар добавлен успешно'})
        response.status_code = 200
        return response

    @restaurant_login_required(current_user)
    def delete(self):
        data = card_delete_data.parse_args()
        card = get_card_product(data['card_id'])
        if card is None:
            response = jsonify({'data': 'Такого товара нет'})
            response.status_code = 200
            return response

        if card.image == '':
            card.image = 'some_image'

        # удаление картинки товара
        file_path = CONFIG.basepath + "application/static/" + card.image
        if os.path.exists(file_path):
            os.remove(file_path)

        delete_card_product(data['card_id'])

        response = jsonify({'data': 'Товар удален успешно'})
        response.status_code = 200
        return response

    @restaurant_login_required(current_user)
    def patch(self):
        data = card_patch_data.parse_args()
        card = get_card_product(data['card_id'])
        if card is None:
            response = jsonify({'data': 'Данный товар не найден'})
            response.status_code = 200
            return response

        change = ''
        for item, key in data.items():
            if item == 'card_id':
                continue
            if key:
                if item == 'name':
                    card.name = key
                elif item == 'price':
                    card.price = key
                elif item == 'image':
                    image = key

                    # сохранение полученной картинки
                    file_path = CONFIG.basepath + 'application/static/' + image.filename
                    if not os.path.exists(file_path):
                        image.save(file_path)

                    # удаление старой картинки
                    if card.image == '':
                        card.image = 'some_image'

                    file_path = CONFIG.basepath + 'application/static/' + card.image
                    if os.path.exists(file_path):
                        os.remove(file_path)

                    card.image = key.filename

                change += item + ', '
        change = change[:-2]

        db.session.commit()

        response = jsonify({'data': f'Следующие данные товара изменены: {change}'})
        response.status_code = 200
        return response


class PassOrders(Resource):
    # заполнение корзины: basket, оплата: paid, кухня: prepared, ready,
    # canceled_restaurant, курьер: delivered, success, canceled_delivery

    # после оплаты поступают на этот урл
    # id_order, name(whole), date,
    # когда заказ оплачен, наверное курьеру(если такое будет) надо тоже показать, что заказ готовится
    parameter_marshaller = {
        "name": fields.String,
        "amount": fields.Integer,
    }

    card_fields = {
        'order_id': fields.Integer,
        'text': fields.String,
        'date': fields.DateTime,
        'address': fields.String,
        'status': fields.String,
        'price': fields.Integer,
        'cards': fields.List(fields.Nested(parameter_marshaller))
    }

    @restaurant_login_required(current_user)
    @marshal_with(card_fields)
    def get(self):
        pass_orders = get_pass_orders()

        # преобразует строки с множеством значений в словари для последующей сериализации
        list_dicts_pass_orders = pass_orders_to_list_dicts(pass_orders)

        return list_dicts_pass_orders


class CurrentOrders(Resource):
    parameter_marshaller = {
        "name": fields.String,
        "amount": fields.Integer,
    }

    card_fields = {
        'order_id': fields.Integer,
        'text': fields.String,
        'date': fields.DateTime,
        'address': fields.String,
        'status': fields.String,
        'price': fields.Integer,
        'cards': fields.List(fields.Nested(parameter_marshaller))
    }

    @restaurant_login_required(current_user)
    @marshal_with(card_fields)
    def get(self):

        current_orders = get_current_orders()

        # преобразует строки с множеством значений в словари для последующей сериализации
        list_dicts_current_orders = current_orders_to_list_dicts(current_orders)

        return list_dicts_current_orders

    # сработает когда нажимают на кнопку рядом с заказом - принято к выполнению, готово, отменить
    @restaurant_login_required(current_user)
    def patch(self):

        data = order_patch_data.parse_args()
        order = Order.query.filter_by(order_id=data['order_id']).first()
        if order is None:
            response = jsonify({'data': 'Заказ не найден'})
            response.status_code = 200
            return response

        if data['action'] == '':
            order.status = 'success'
        elif data['action'] == '':
            order.status = 'success'
        elif data['action'] == '':
            order.status = 'success'

        db.session.commit()
        response = jsonify({'data': 'Статус заказа изменен'})
        response.status_code = 200
        return response


api_restaurant.add_resource(Index, '/')
api_restaurant.add_resource(Cards, '/cards')
api_restaurant.add_resource(CurrentOrders, '/current_orders')
api_restaurant.add_resource(PassOrders, '/pass_orders')
