from flask import Blueprint, g
from flask_restful import Api, Resource, reqparse

from models.projects import Project as ProjectModel
from models.hosts import Host as HostModel
from models.users import User as UserModel
from libs.services import DeployService

import time

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
        project_id = args['project_id']
        # 版本
        branch_id = args['commit'][0]
        commit_id = args['commit'][1]
        # 仓库信息 eg. git_repo
        _project = g.gl.projects.get(project_id)
        ssh_url_to_repo = _project.attributes.get('ssh_url_to_repo')
        name = _project.attributes.get('name')
        # 部署信息 eg. 部署前后需要执行的命令
        project = ProjectModel.get(project_id)
        proj_name = project.name
        proj_before_checkout = project.before_checkout
        proj_after_checkout = project.after_checkout
        proj_before_deploy = project.before_deploy
        proj_after_deploy = project.after_deploy
        proj_hosts = [h.ip_addr for h in project.hosts if h.env == 1]
        if args['env'] == 'True':
            proj_hosts = [h.ip_addr for h in project.hosts if h.env == 0]
        # 记录信息 eg. 发布者、时间
        user = UserModel.get(args['current_user'])
        user_name = user.gitlab_username
        deploy_time = time.time()

        ds = DeployService()
        return ds.test()


api.add_resource(Deploy, '/deploys/<int:id>', endpoint='deploy')
api.add_resource(DeployList, '/deploys', endpoint='deploys')
