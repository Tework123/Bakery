import time

from flask import jsonify, url_for
from flask_restful import Resource, fields, marshal_with

from application.email.email import send_email
from application.main import api_main
from application.models import CardProduct
from start_app import CONFIG


class Index(Resource):
    card_fields = {
        'card_id': fields.Integer,
        'name': fields.String,
        'price': fields.Integer,
        'image': fields.String
    }

    @marshal_with(card_fields)
    def get(self):
        cards = CardProduct.query.all()

        cards_dicts = []
        for row in cards:
            row = {'card_id': row.card_id, 'name': row.name, 'price': row.price,
                   'image': url_for('static', filename=row.image)}
            cards_dicts.append(row)

        return cards_dicts


api_main.add_resource(Index, '/')
