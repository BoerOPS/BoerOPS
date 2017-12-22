from flask import Blueprint, g
from flask_restful import Api, Resource, reqparse

from models.projects import Project as ProjectModel
from models.hosts import Host as HostModel
from libs.services import DeployService

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
        parser.add_argument('current_user', help='required')
        parser.add_argument('env', help='required')
        parser.add_argument('commit', action='append', help='required')
        args = parser.parse_args()
        print('---args--->', args)
        print('---args--->', type(args['env']))
        # {'commit_id': None, 'branch_id': None, 'project_id': '121'}
        _project = g.gl.projects.get(args['project_id'])
        ssh_url_to_repo = _project.attributes.get('ssh_url_to_repo')
        name = _project.attributes.get('name')
        _hosts = ProjectModel.get(args['project_id']).hosts
        if args['env'] == 'True':
            hosts = [h.ip_addr for h in _hosts if h.env == 0]
        else:
            hosts = [h.ip_addr for h in _hosts if h.env == 1]
        print('---hosts--->', hosts)
        ds = DeployService()
        return ds.test()


api.add_resource(Deploy, '/deploys/<int:id>', endpoint='deploy')
api.add_resource(DeployList, '/deploys', endpoint='deploys')
