import datetime
import json

from flask import jsonify
from flask_login import login_user, current_user

from application import db
from application.cards import api_cards
from application.models import Users, CardProducts
from flask_restful import Resource, marshal_with, fields


class Index(Resource):
    def get(self):
        time = datetime.datetime.now()
        time = json.dumps(time, default=str)
        response = jsonify({'data': time})
        return response


api_cards.add_resource(Index, '/')
