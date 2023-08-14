import logging

from flask import jsonify, url_for
from flask_login import current_user
from flask_restful import Resource, fields, marshal_with

from application.main.service import get_all_cards, get_one_card
from application.auth.auth import login_required
from application.main import api_main


class Cards(Resource):
    card_fields = {
        'card_id': fields.Integer,
        'name': fields.String,
        'price': fields.Integer,
        'image': fields.String
    }

    @marshal_with(card_fields)
    def get(self):
        cards = get_all_cards()

        cards_dicts = []
        for row in cards:
            row = {'card_id': row.card_id, 'name': row.name, 'price': row.price,
                   'image': url_for('static', filename=row.image)}
            cards_dicts.append(row)

        log = logging.getLogger('tester.sub')

        for i in cards_dicts:
            log.warning(i)

        return cards_dicts


# надо посмотреть, что выводит фронт в картинках, тестировать на компе, а то этот долго собирает
class Card(Resource):
    card_fields = {
        'card_id': fields.Integer,
        'name': fields.String,
        'price': fields.Integer,
        'image': fields.String
    }

    @marshal_with(card_fields)
    def get(self, card_id):
        card = get_one_card(card_id)
        if card is None:
            response = jsonify({'data': 'Такого товара нет'})
        else:
            response = card

        response.status_code = 200
        return jsonify({'data': response})


api_main.add_resource(Cards, '/')
api_main.add_resource(Card, '/<int:card_id>')
