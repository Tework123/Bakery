import time

from flask import jsonify
from flask_restful import Resource, fields, marshal_with

from application.email.email import send_email
from application.main import api_main
from application.models import CardProduct
from start_app import CONFIG


class Index(Resource):
    card_fields = {
        'card_id': fields.Integer,
        'name': fields.String,
        'price': fields.Price,
        'image': fields.String
    }

    @marshal_with(card_fields)
    def get(self):
        cards = CardProduct.query.all()

        # import base64
        # # либо так отправляем, либо другими способами, вот здесь можно и закешировать (у юзера, а не у админа)
        # for card in cards:
        #     file_path = CONFIG.basepath + 'application/static/' + card.card_image
        #     with open(file_path, "rb") as image_file:
        #         my_string = base64.b64encode(image_file.read()).decode("utf-8")
        #
        #     card.card_image = my_string
        #
        # # что-то из этого должно декодировать картинку и показывать на сайте(но это js будет делать)
        # for card in cards:
        #     my_string = base64.b64decode(card.card_image)
        #     # with open(card.card_name, 'wb') as file:
        #     #     file.write(my_string)
        #     card.card_image = my_string
        # # card.card_image = url_for('static', filename=card.card_image)
        return cards
    # при нажатии на карточку должно быть перенаправление на url с карточкой cargs/1 , на фронте должна
    # отрываться окошко


api_main.add_resource(Index, '/')
