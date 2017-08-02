from flask import Blueprint
from flask_restful import Api, Resource, url_for

bp = Blueprint('deploy', __name__)
api = Api(bp)

class Deploy(Resource):
    def get(self, id):
        return {'task': 'done'}

api.add_resource(Deploy, '/deploy/<int:id>')