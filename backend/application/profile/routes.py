import sqlalchemy
from flask import jsonify
from flask_login import current_user
from sqlalchemy import cast, and_

from application import db
from application.auth.auth import login_required

from application.models import User, CardProduct, Order, OrderProduct
from flask_restful import Resource, marshal_with, fields

from application.profile import api_profile
from application.profile.fields_validation import profile_data, email_validation
from application.profile.helpers import orders_to_list_dicts
from application.profile.service import get_user, get_orders


class Profile(Resource):
    profile_fields = {
        'email': fields.String,
        'address': fields.String
    }

    @login_required(current_user)
    @marshal_with(profile_fields)
    def get(self):
        user = get_user(current_user.user_id)
        return user

    @login_required(current_user)
    def patch(self):
        data = profile_data.parse_args()

        change = ''
        for item, key in data.items():

            if key:
                if item == 'email':
                    email_validation(data)
                    current_user.email = key
                if item == 'address':
                    current_user.address = key

                change += item + ', '
        change = change[:-2]

        db.session.commit()

        response = jsonify({'data': f'Следующие данные товара изменены: {change}'})
        response.status_code = 200
        return response


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
        orders = get_orders(current_user.user_id)

        # преобразует строки с множеством значений в словари для последующей сериализации
        list_dicts_orders = orders_to_list_dicts(orders)

        return list_dicts_orders


# этот запрос скорее всего не нужен, в другом уже все данные отправлены
class OrderChoose(Resource):
    orders_fields = {
        'data': fields.String,
        'order_id': fields.Integer,
        'status': fields.String,
        'price': fields.Integer,
        'name': fields.String,
        'amount': fields.String,
        'image': fields.String
    }

    @login_required(current_user)
    @marshal_with(orders_fields)
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


api_profile.add_resource(Profile, '/')
api_profile.add_resource(Orders, '/orders')
api_profile.add_resource(OrderChoose, '/orders/<int:order_id>')
