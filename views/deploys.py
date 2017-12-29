from flask import Blueprint, g, current_app
from flask_restful import Api, Resource, reqparse

from models.projects import Project as ProjectModel
from models.hosts import Host as HostModel
from models.users import User as UserModel
from models.deploys import Deploy as DeployModel
from libs.services import DeployService

import time

bp = Blueprint('deploy', __name__)
api = Api(bp)

parser = reqparse.RequestParser()


class Deploy(Resource):
    def get(self, id):
        return {'task': 'done'}

    def delete(self, id):
        pass


class DeployList(Resource):
    def get(self):
        pass

    def post(self):
        parser.add_argument('project_id', help='required')
        parser.add_argument('current_user', help='required')
        parser.add_argument('env', help='required')
        parser.add_argument('version_intro', help='required')
        parser.add_argument('commit', action='append', help='required')
        args = parser.parse_args()

        project_id = int(args['project_id'])
        branch_id = args['commit'][0]
        commit_id = args['commit'][1]
        user_id = int(args['current_user'])
        environment = 0 if args['env'] == 'True' else 1

        _project = g.gl.projects.get(project_id)
        project_args = {
            'name': _project.attributes.get('name'),
            'repo_ssh_url': _project.attributes.get('ssh_url_to_repo')
        }
        # deploy = DeployModel.query.filter(
        #     DeployModel.project_id == project_id, DeployModel.status != 5,
        #     DeployModel.env == environment).first()
        # if deploy is not None:
        #     return {'status': 0, 'msg': '当前项目在当前环境上有未完成的部署任务，请稍后！'}
        deploy = DeployModel.create(
            status=0,
            project_id=project_id,
            branch_id=branch_id,
            commit_id=commit_id,
            env=environment,
            user_id=user_id,
            introduce=args['version_intro'])
        config = current_app.config['DEPLOYMENT']
        ds = DeployService(deploy, config, project_args)
        # return ds.run()
        return ds.step_3()


api.add_resource(Deploy, '/deploys/<int:id>', endpoint='deploy')
api.add_resource(DeployList, '/deploys', endpoint='deploys')
