from flask import Blueprint, request
from flask_restful import Api, Resource, url_for

from models.hosts import Host

bp = Blueprint('deploy', __name__)
api = Api(bp)

class Host(Resource):
    def get(self, id):
        return {'task': 'done'}

class HostList(Resource):
    def get(self):
        # env = request.args.get('env')
        pass


api.add_resource(Host, '/hosts/<int:id>', endpoint='host')
api.add_resource(HostList, '/hosts', endpoint='hosts')