import datetime
import json

from flask import jsonify, request
from flask_login import login_user

from application import db
from application.models import Users, Card
from flask_restful import Resource, reqparse, abort, marshal_with, fields

from . import api_main
from .fields_validation import register_data, register_validation, login_data, login_validation, card_data


# эти url наверное будут уже на фронте, их не надо передавать
# menu = [['Начальная страница', '/home'], ['О нас', '/we'], ['Войти', '/login']]


class Index(Resource):
    def get(self):
        time = datetime.datetime.now()
        time = json.dumps(time, default=str)
        response = jsonify({'data': time})
        return response


class Register(Resource):
    def post(self):
        data = register_data.parse_args()
        register_validation(data)
        user = Users(name=data['name'], email=data['email'], password=data['password'], phone=data['phone'])
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        response = jsonify({'data': 'Регистрация прошла успешно'})
        response.status_code = 200
        return response


class Login(Resource):
    def post(self):
        data = login_data.parse_args()
        login_validation(data)
        user = Users.query.filter_by(email=data['email']).first()
        login_user(user)
        response = jsonify({'data': 'login success'})
        response.status_code = 200
        return response


class CardActions(Resource):
    def post(self):
        data = card_data.parse_args()
        card = Card(name=data['name'], price=data['price'])
        db.session.add(card)
        db.session.flush()
        db.session.commit()
        response = jsonify({'data': 'Товар добавлен успешно'})
        response.status_code = 200
        return response

    card_fields = {
        'name': fields.String,
        'price': fields.Price
    }

    @marshal_with(card_fields)
    def get(self):
        card = Card.query.all()
        return card


api_main.add_resource(Index, '/')
api_main.add_resource(Login, '/login')
api_main.add_resource(Register, '/register')
api_main.add_resource(CardActions, '/card')
