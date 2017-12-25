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
        # 版本
        branch_id = args['commit'][0]
        commit_id = args['commit'][1]
        user_id = int(args['current_user'])
        # 仓库信息 eg. git_repo
        _project = g.gl.projects.get(project_id)
        ssh_url_to_repo = _project.attributes.get('ssh_url_to_repo')
        name = _project.attributes.get('name')
        # 部署信息 eg. 部署前后需要执行的命令
        project = ProjectModel.get(project_id)
        proj_name = project.name
        proj_before_cmd = project.before_cmd
        proj_after_cmd = project.after_cmd
        proj_hosts = [h.ip_addr for h in project.hosts if h.env == 1]
        environment = 1
        if args['env'] == 'True':
            environment = 0
            proj_hosts = [h.ip_addr for h in project.hosts if h.env == 0]
        # 记录信息 eg. 发布者、时间
        user = UserModel.get(user_id)
        user_name = user.gitlab_username
        deploy = DeployModel.first(
            project_id=project_id, status=0, env=environment)
        if deploy is not None:
            return {'status': 0, 'msg': '当前项目在当前环境上有未完成的部署任务，请稍后！'}
        deploy = DeployModel.create(
            status=0,
            project_id=project_id,
            branch_id=branch_id,
            commit_id=commit_id,
            env=environment,
            user_id=user_id,
            introduce=args['version_intro'])
        checkout_path = current_app.config['CHECKOUT_PATH']
        deploy_path = current_app.config['DEPLOY_PATH']
        ds = DeployService(deploy, checkout_path, deploy_path)
        return ds.step_1(ssh_url_to_repo, name)


api.add_resource(Deploy, '/deploys/<int:id>', endpoint='deploy')
api.add_resource(DeployList, '/deploys', endpoint='deploys')
