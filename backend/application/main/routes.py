from flask import jsonify, request
from flask_login import login_user

from application import db
from application.main import bp
from application.models import Users

menu = [['Начальная страница', '/home'], ['О нас', '/we'], ['Войти', '/login']]


@bp.route('/', methods=['GET'])
def index():
    data = 'main index'
    response = jsonify({'data': data})
    response.status_code = 200
    return response


@bp.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    user = Users(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.flush()
    db.session.commit()

    response = jsonify({'data': 'register success'})
    response.status_code = 200
    return response


@bp.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    user = db.session.query(Users).filter_by(email=data['email']).first()
    login_user(user)
    response = jsonify({'data': 'login success'})
    response.status_code = 200
    return response