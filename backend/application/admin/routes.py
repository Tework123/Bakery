from flask import jsonify

from application.admin import bp

menu = [['Начальная страница', '/home'], ['О нас', '/we'], ['Войти', '/login']]


@bp.route('/', methods=['GET'])
def index():
    data = 'test'
    response = jsonify({'data': data})
    response.status_code = 200
    return response


@bp.route('/login', methods=['GET', 'POST'])
def login():
    data = 'success'
    response = jsonify({'data': data})
    response.status_code = 200
    return response