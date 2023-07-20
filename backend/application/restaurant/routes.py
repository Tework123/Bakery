import os

import sqlalchemy
from flask import jsonify
from flask_login import current_user
from flask_restful import Resource, fields, marshal_with
from sqlalchemy import or_, cast

from application import db
from application.auth.auth import admin_login_required
from application.models import CardProduct, Order, OrderProduct
from application.restaurant import api_restaurant
from application.restaurant.fields_validation import card_data, card_delete_data, card_patch_data
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

    # здесь отправка картинок и всего остального для работников ресторана
    @marshal_with(card_fields)
    def get(self):
        cards = CardProduct.query.all()

        import base64
        # либо так отправляем, либо другими способами, вот здесь можно и закешировать (у юзера, а не у админа)
        # for card in cards:
        #     file_path = CONFIG.basepath + 'application/static/' + card.card_image
        #     with open(file_path, "rb") as image_file:
        #         my_string = base64.b64encode(image_file.read()).decode("utf-8")
        #
        #     card.card_image = my_string
        # card.card_image = url_for('static', filename=card.card_image)

        # выводятся данные и на фронте расставляются в табличку с кнопками удалить, добавить
        return cards

    @admin_login_required(current_user)
    def post(self):
        data = card_data.parse_args()
        image = data['image']

        # сохранение полученной картинки
        file_path = CONFIG.basepath + 'application/static/' + image.filename

        if not os.path.exists(file_path):
            data['image'].save(file_path)
        try:
            card = CardProduct(name=data['name'], price=data['price'], image=image.filename)
            db.session.add(card)
            db.session.flush()
        except:
            db.session.rollback()
            response = jsonify({'data': 'Названия товара и картинки должны быть уникальными'})
            response.status_code = 400
            return response

        db.session.commit()
        response = jsonify({'data': 'Товар добавлен успешно'})
        response.status_code = 200
        return response

    @admin_login_required(current_user)
    def delete(self):
        data = card_delete_data.parse_args()
        card = CardProduct.query.filter_by(card_id=data['card_id']).first()
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

        CardProduct.query.filter_by(card_id=data['card_id']).delete()
        db.session.commit()

        response = jsonify({'data': 'Товар удален успешно'})
        response.status_code = 200
        return response

    @admin_login_required(current_user)
    def patch(self):
        data = card_patch_data.parse_args()
        card = CardProduct.query.filter_by(card_id=data['card_id']).first()
        if card:
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
        else:
            response = jsonify({'data': 'Данный товар не найден'})
            response.status_code = 200
            return response


class Orders(Resource):
    # заполнение корзины: basket, оплата: paid, кухня: prepared, ready,
    # canceled_restaurant, курьер: delivered, success, canceled_delivery

    # после оплаты поступают на этот урл
    # id_order, name(whole), date,
    # когда заказ оплачен, наверное курьеру(если такое будет) надо тоже показать, что заказ готовится
    card_fields = {
        'order_id': fields.Integer,
        'text': fields.String,
        'date': fields.DateTime,
        'address': fields.String,
        'amount': fields.String,
        'name': fields.String,
    }

    @admin_login_required(current_user)
    @marshal_with(card_fields)
    def get(self):
        orders = db.session.query(Order.order_id,
                                  Order.text,
                                  Order.address,
                                  Order.date,
                                  db.func.string_agg(CardProduct.name, ', ').label('name'),
                                  db.func.string_agg(cast(OrderProduct.amount, sqlalchemy.String), ', ')
                                  .label('amount')) \
            .join(OrderProduct, Order.order_id == OrderProduct.order_id) \
            .join(CardProduct, OrderProduct.card_id == CardProduct.card_id) \
            .group_by(Order.order_id,
                      Order.text,
                      Order.address,
                      Order.date, ) \
            .where(or_(Order.status == 'paid',
                       Order.status == 'prepared',
                       Order.status == 'ready',
                       Order.status == 'canceled_restaurant',
                       Order.status == 'delivered',
                       Order.status == 'success',
                       Order.status == 'canceled_delivery',
                       )).all()
        return orders

    @admin_login_required(current_user)
    def patch(self):
        # нажимаем на кнопку рядом с заказом - принято к выполнению, готово, отменить
        # с курьерами уже потом сделаем, после показа
        pass


api_restaurant.add_resource(Index, '/')
api_restaurant.add_resource(Cards, '/cards')
api_restaurant.add_resource(Orders, '/orders')
