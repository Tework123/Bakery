import os

from flask import jsonify, request, url_for
from flask_login import current_user
from flask_restful import Resource, fields, marshal_with

from application import db
from application.admin import api_admin
from application.admin.fields_validation import \
    delete_admin_data, create_restaurant_data, create_restaurant_validation
from application.auth.auth import admin_login_required
from application.models import CardProduct, User
from config import Config


class Index(Resource):
    @admin_login_required(current_user)
    def get(self):
        response = jsonify({'data': 'admin panel here'})
        return response


class CreateRestaurant(Resource):
    restaurant_fields = {
        'user_id': fields.Integer,
        'email': fields.String,
        'role': fields.String
    }

    @admin_login_required(current_user)
    @marshal_with(restaurant_fields)
    def get(self):
        admins = User.query.filter_by(role='restaurant').all()
        return admins

    @admin_login_required(current_user)
    def post(self):
        data = create_restaurant_data.parse_args()
        create_restaurant_validation(data)
        user = User(email=data['email'], role='restaurant')
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        response = jsonify({'data': 'Работник пекарни создан успешно'})
        response.status_code = 200
        return response

    @admin_login_required(current_user)
    def delete(self):
        data = delete_admin_data.parse_args()
        User.query.filter_by(email=data['email']).delete()
        db.session.commit()
        response = jsonify({'data': 'Работник пекарни удален успешно'})
        response.status_code = 403
        return response


class SiteStatistics(Resource):

    # тут наверное нужно ссылка на яндекс метрику
    @admin_login_required(current_user)
    def get(self):
        return jsonify({'data': 'some statistics'})


api_admin.add_resource(Index, '/')
api_admin.add_resource(CreateRestaurant, '/create_restaurant')
api_admin.add_resource(SiteStatistics, '/site_statistics')
