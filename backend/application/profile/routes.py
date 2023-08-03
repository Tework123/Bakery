import time

import sqlalchemy
from flask import jsonify, request, url_for
from flask_login import login_user, current_user
from sqlalchemy import text, cast, or_

from application import db
from application.auth.auth import login_required

from application.models import User, CardProduct, Order, OrderProduct
from flask_restful import Resource, marshal_with, fields

from application.profile import api_profile
from application.profile.helpers import orders_to_list_dicts
from start_app import CONFIG


class Orders(Resource):
    parameter_marshaller = {
        "name": fields.String,
        "amount": fields.Integer,
        'image': fields.String
    }

    card_fields = {
        'order_id': fields.Integer,
        'text': fields.String,
        'date': fields.DateTime,
        'status': fields.String,
        'price': fields.Integer,
        'cards': fields.List(fields.Nested(parameter_marshaller))
    }

    @login_required(current_user)
    @marshal_with(card_fields)
    def get(self):
        orders = (db.session.query(Order.order_id,
                                   Order.text,
                                   Order.date,
                                   Order.status,
                                   db.func.sum(OrderProduct.price).label('price'),
                                   db.func.string_agg(CardProduct.name, ', ').label('name'),
                                   db.func.string_agg(cast(OrderProduct.amount, sqlalchemy.String), ', ')
                                   .label('amount'),
                                   db.func.string_agg(cast(CardProduct.image, sqlalchemy.String), ', ')
                                   .label('image')).
                  join(OrderProduct, Order.order_id == OrderProduct.order_id)
                  .join(CardProduct, OrderProduct.card_id == CardProduct.card_id)
                  .group_by(Order.order_id,
                            Order.text,
                            Order.date)
                  .where(Order.user_id == current_user.user_id).all())

        # преобразует строки с множеством значений в словари для последующей сериализации
        list_dicts_orders = orders_to_list_dicts(orders)

        return list_dicts_orders


# кнопка - заказать еще раз, получается по id заказа достается вся информация и добавляется в корзину, нужно поменять  id заказа
# и статус ставится на basket, если оплачивает - paid

class PassOrders(Resource):
    profile_fields = {
        'order_id': fields.Integer,
        'date': fields.DateTime,
        'price': fields.Integer,
        'status': fields.String,
        'image': fields.String
    }

    @login_required(current_user)
    @marshal_with(profile_fields)
    def get(self):
        pass_orders = db.session.query(Order.order_id,
                                       Order.date,
                                       db.func.sum(OrderProduct.price).label('price'),
                                       Order.status). \
            join(OrderProduct, Order.order_id == OrderProduct.order_id) \
            .group_by(Order.order_id, Order.date, Order.status) \
            .where(Order.user_id == current_user.user_id, or_(Order.status == 'canceled_restaurant',
                                                              Order.status == 'delivered',
                                                              Order.status == 'success',
                                                              Order.status == 'canceled_delivery')).all()

        # pass_orders_dicts = []
        # for row in pass_orders:
        #     row = {'card_id': row.card_id, 'name': row.name, 'price': row.price,
        #            'image': url_for('static', filename=row.image)}
        #     pass_orders_dicts.append(row)

        return pass_orders


class OrderChoose(Resource):
    profile_fields = {
        'data': fields.String,
        'order_id': fields.Integer,
        'status': fields.String,
        'price': fields.Integer,
        'name': fields.String,
        'amount': fields.String,
        'image': fields.String

    }

    @login_required(current_user)
    @marshal_with(profile_fields)
    def get(self, order_id):
        order = Order.query.filter_by(user_id=current_user.user_id, order_id=order_id).first()
        if order is None:
            response = {'data': 'У вас нет такого заказа'}
            return response, 200

        order_choose = db.session.query(Order.order_id,
                                        Order.status,
                                        Order.date,
                                        db.func.sum(OrderProduct.price).label('price'),
                                        db.func.string_agg(CardProduct.name, ', ').label('name'),
                                        db.func.string_agg(cast(OrderProduct.amount, sqlalchemy.String), ', ')
                                        .label('amount')) \
            .join(OrderProduct, Order.order_id == OrderProduct.order_id) \
            .join(CardProduct, OrderProduct.card_id == CardProduct.card_id) \
            .group_by(Order.order_id, Order.status).where(Order.order_id == order_id).all()

        return order_choose


class CurrentOrders(Resource):
    card_fields = {
        'order_id': fields.Integer,
        'text': fields.String,
        'date': fields.DateTime,
        'address': fields.String,
        'amount': fields.String,
        'name': fields.String,
        'status': fields.String,
        'image': fields.String

    }

    @login_required(current_user)
    @marshal_with(card_fields)
    def get(self):
        current_orders = db.session.query(Order.order_id,
                                          Order.text,
                                          Order.address,
                                          Order.date,
                                          Order.status,
                                          db.func.string_agg(CardProduct.name, ', ').label('name'),
                                          db.func.string_agg(cast(OrderProduct.amount, sqlalchemy.String), ', ')
                                          .label('amount')) \
            .join(OrderProduct, Order.order_id == OrderProduct.order_id) \
            .join(CardProduct, OrderProduct.card_id == CardProduct.card_id) \
            .group_by(Order.order_id,
                      Order.text,
                      Order.address,
                      Order.date) \
            .where(Order.user_id == current_user.user_id,
                   or_(Order.status == 'paid',
                       Order.status == 'prepared',
                       Order.status == 'ready',
                       Order.status == 'delivered',
                       )).all()
        return current_orders


api_profile.add_resource(PassOrders, '/pass_orders')
api_profile.add_resource(Orders, '/orders')
api_profile.add_resource(OrderChoose, '/orders/<int:order_id>')
api_profile.add_resource(CurrentOrders, '/current_orders')
