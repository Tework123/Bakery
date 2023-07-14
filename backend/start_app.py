from flask import jsonify, request
from flask_restful import Resource, Api

from config import DevelopmentConfig
from config import ProductionConfig

from application import create_app

CONFIG = DevelopmentConfig

app = create_app(CONFIG)


@app.route('/admin/privet', methods=['POST', 'GET'])
def add_image():
    if request.method == 'POST':
        image = request.files['card_image']
        print(image)
    return jsonify({'data': '123'})