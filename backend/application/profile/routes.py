import sqlalchemy
from flask import jsonify, request
from flask_login import login_user, current_user
from sqlalchemy import text, cast

from application import db
from application.auth.auth import login_required

from application.models import User, CardProduct, Order, OrderProduct
from flask_restful import Resource, marshal_with, fields

from application.profile import api_profile
from start_app import CONFIG


class Index(Resource):
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
            .where(Order.user_id == current_user.user_id, Order.status != 'basket').all()

        return profile_data


class OrderChoose(Resource):
    profile_fields = {
        'order_id': fields.Integer,
        'status': fields.String,
        'price': fields.Integer,
        'name': fields.String,
        'amount': fields.String,
    }

    @login_required(current_user)
    @marshal_with(profile_fields)
    def get(self, order_id):
        print(order_id)

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


# наверное нужно отдельную вкладку сделать для обычного пользователя, хотя можно и во вкладке профиля
# заходишь туда, а на всем экране твои заказы
# внизу история выполненных заказов
class CurrentOrders(Resource):
    def get(self):
        # надо вернуть id_order, price общую и каждого товара, количество каждой позиции,
        # также нужно вернуть каждый товар,
        # возможно с фото, address, status

        # хотя можно тоже при клике на него открывается новое окно или новая страница, а там уже подробности
        # хотя много заказов висеть в готовке вряд ли у кого-то будет, поэтому можно даже картинки подгрузить
        current_orders = db.session.query()
        pass


api_profile.add_resource(Index, '/')
api_profile.add_resource(OrderChoose, '/<int:order_id>')
api_profile.add_resource(CurrentOrders, '/current_orders')

# верхняя url не так как надо работает, надо такие урл сделать:

# /current_orders вернет текущие заказы(где статус != success и не баскет)
# /pass_orders история заказов(где статус == success)
# основная url пока не понятно что вернет
