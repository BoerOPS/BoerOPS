from flask import Blueprint, g
from flask_restful import Api, Resource, reqparse

from models.projects import Project as ProjectModel
from models.hosts import Host as HostModel

bp = Blueprint('deploy', __name__)
api = Api(bp)

parser = reqparse.RequestParser()


class Deploy(Resource):
    def get(self, id):
        return {'task': 'done'}


class DeployList(Resource):
    def get(self):
        pass

    def post(self):
        parser.add_argument('project_id', help='required')
        parser.add_argument('branch_id', help='required')
        parser.add_argument('commit_id', help='required')
        args = parser.parse_args()
        _project = g.gl.projects.get(id(args['project_id']))
        repo_url = _project.attributes.get('repo_url')


api.add_resource(Deploy, '/deploy/<int:id>')
