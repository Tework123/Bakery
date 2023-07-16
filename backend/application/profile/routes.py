import datetime
import json

from flask import jsonify
from flask_login import login_user, current_user

from application import db
from application.auth.auth import login_required

from application.models import User, CardProduct, Order, OrderProduct
from flask_restful import Resource, marshal_with, fields

from application.profile import api_profile
from start_app import CONFIG


class Index(Resource):
    profile_fields = {
        'order_id': fields.Integer,
        'user_id': fields.Integer,
        'card_id': fields.Integer,
        'amount': fields.Integer,
        'card_name': fields.String,
        'card_image': fields.String,
        'card_price': fields.Price
    }

    @login_required(current_user)
    @marshal_with(profile_fields)
    def get(self):
        print(current_user)
        # персональная информация: email, телефон(потом)
        # на одной странице история заказов
        # можно изменять информация прямо на этой страничке
        profile_data = db.session.query(Order.order_id, Order.date, CardProduct.card_name,
                                        (CardProduct.card_price * OrderProduct.amount).label('card_price')).join(
            OrderProduct,
            Order.order_id == OrderProduct.order_id).join(
            CardProduct, OrderProduct.card_id == CardProduct.card_id).where(
            Order.user_id == current_user.user_id, Order.status is True).all()

        return profile_data


api_profile.add_resource(Index, '/')