import datetime
import json

from flask import jsonify
from flask_login import login_user, current_user

from application import db
from application.cards import api_cards
from application.models import User, CardProduct
from flask_restful import Resource, marshal_with, fields


class Index(Resource):
    card_fields = {
        'card_id': fields.Integer,
        'card_name': fields.String,
        'card_price': fields.Price,
        'card_image': fields.String
    }

    @marshal_with(card_fields)
    def get(self, card_id):
        card = CardProduct.query.filter_by(card_id=card_id).first()
        if card is None:
            response = jsonify({'data': 'Такого товара нет'})
        else:
            response = card

        response.status_code = 200
        return response


api_cards.add_resource(Index, '/<int:card_id>')