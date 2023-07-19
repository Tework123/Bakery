import os

from flask import jsonify, request, url_for
from flask_login import current_user
from flask_restful import Resource, fields, marshal_with

from application import db
from application.admin import api_admin
from application.admin.fields_validation import \
    create_admin_data, create_admin_validation, delete_admin_data
from application.auth.auth import admin_login_required
from application.models import CardProduct, User
from config import Config


class Index(Resource):
    @admin_login_required(current_user)
    def get(self):
        response = jsonify({'data': 'admin panel here'})
        return response


class CreateRestaurant(Resource):
    admins_fields = {
        'id_user': fields.Integer,
        'email': fields.String,
        # 'phone': fields.String,
        'role': fields.String
    }

    @admin_login_required(current_user)
    @marshal_with(admins_fields)
    def get(self):
        admins = User.query.filter_by(role='restaurant').all()
        return admins

    @admin_login_required(current_user)
    def post(self):
        if current_user.email != Config.MAIN_ADMIN_EMAIL:
            response = jsonify({'data': 'Вы не являетесь главным админом'})
            response.status_code = 403
            return response

        data = create_admin_data.parse_args()
        create_admin_validation(data)
        user = User(email=data['email'], role='restaurant')
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        response = jsonify({'data': 'Работник пекарни создан успешно'})
        response.status_code = 200
        return response

    @admin_login_required(current_user)
    def delete(self):
        if current_user.email != Config.MAIN_ADMIN_EMAIL:
            response = jsonify({'data': 'Вы не являетесь главным админом'})
            response.status_code = 403
            return response

        data = delete_admin_data.parse_args()
        User.query.filter_by(email=data['email']).delete()
        db.session.commit()
        response = jsonify({'data': 'Работник пекарни удален успешно'})
        response.status_code = 403
        return response


api_admin.add_resource(Index, '/')
api_admin.add_resource(CreateRestaurant, '/create_admin')
