import time

from flask import jsonify, url_for, session, request, make_response
from flask_restful import Resource, fields, marshal_with

from application.email.email import send_email, send_email_authentication, celery_task
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


class Cards(Resource):
    card_fields = {
        'card_id': fields.Integer,
        'name': fields.String,
        'price': fields.Integer,
        'image': fields.String
    }

    @marshal_with(card_fields)
    def get(self, card_id):
        card = CardProduct.query.filter_by(card_id=card_id).first()
        if card is None:
            response = jsonify({'data': 'Такого товара нет'})
        else:
            response = card

        response.status_code = 200
        return jsonify({'data': response})


class Test(Resource):
    def get(self):
        response = jsonify({'data': '123'})

        session['email'] = '123'
        # можно в куки фласк логина попробовать роль юзера запихать
        # я могу ему роль передать при первом get запросе  /main на картинки
        # если что, можно в заголовке или в json отправить роль, если зарегистрирован

        count = int(request.cookies.get('visitors count', 0))
        count = count + 1
        output = 'You visited this page for ' + str(count) + ' times'
        response.set_cookie('visitors count', str(count), max_age=2000000)
        return jsonify({'data': output})


class Email(Resource):

    def get(self):
        celery_task()
        return '123'
        # send_email_authentication(time.time(), code=123)


api_main.add_resource(Index, '/')
api_main.add_resource(Cards, '/<int:card_id>')
api_main.add_resource(Test, '/test')

api_main.add_resource(Email, '/email')
