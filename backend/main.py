from flask import jsonify
from flask_restful import Resource, Api

from start_app import app

api = Api()
api_routes(api)
api.init_app(app)

class Index(Resource):
    def get(self):
        response = jsonify({'data': 'main page here'})
        return response


api.add_resource(Index, '/')
