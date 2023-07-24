import sqlalchemy
from flask import jsonify, request
from flask_login import login_user, current_user
from sqlalchemy import text, cast, or_

from application import db
from application.auth.auth import login_required

from application.models import User, CardProduct, Order, OrderProduct
from flask_restful import Resource, marshal_with, fields

from application.profile import api_profile
from start_app import CONFIG


class PassOrders(Resource):
    profile_fields = {
        'order_id': fields.Integer,
        'date': fields.DateTime,
        'price': fields.Integer,
        'status': fields.String
    }

    @login_required(current_user)
    @marshal_with(profile_fields)
    def get(self):
        profile_data = db.session.query(Order.order_id,
                                        Order.date,
                                        db.func.sum(OrderProduct.price).label('price'),
                                        Order.status). \
            join(OrderProduct, Order.order_id == OrderProduct.order_id) \
            .group_by(Order.order_id, Order.date, Order.status) \
            .where(Order.user_id == current_user.user_id, or_(Order.status == 'canceled_restaurant',
                                                              Order.status == 'delivered',
                                                              Order.status == 'success',
                                                              Order.status == 'canceled_delivery')).all()

        return profile_data


class OrderChoose(Resource):
    profile_fields = {
        'data': fields.String,
        'order_id': fields.Integer,
        'status': fields.String,
        'price': fields.Integer,
        'name': fields.String,
        'amount': fields.String,
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
        'status': fields.String

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
api_profile.add_resource(OrderChoose, '/pass_orders/<int:order_id>')
api_profile.add_resource(CurrentOrders, '/current_orders')
