from flask import jsonify
from flask_restful import Resource, fields, marshal_with

from application.main import api_main
from application.models import CardProducts


# ссылки на меню наверное будет у фронта

class Index(Resource):
    card_fields = {
        'card_id': fields.Integer,
        'card_name': fields.String,
        'card_price': fields.Price,
        'card_image': fields.String
    }

    @marshal_with(card_fields)
    def get(self):
        cards = CardProducts.query.all()
        return cards
    # при нажатии на карточку должно быть перенаправление на url с карточкой cargs/1 , на фронте должна
    # отрываться окошко


api_main.add_resource(Index, '/')
