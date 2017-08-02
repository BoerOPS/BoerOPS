from flask import Blueprint
from flask_restful import Api, Resource, url_for

bp = Blueprint('user', __name__)
api = Api(bp)

class User(Resource):
    def get(self, id):
        return {'task': 'done'}

api.add_resource(User, '/user/<int:id>')