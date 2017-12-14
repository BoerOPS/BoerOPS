from flask import Blueprint, render_template, request, jsonify, g
# from flask_login import login_required
from flask_restful import Api, Resource, abort, reqparse

import gitlab

bp = Blueprint('project', __name__)
api = Api(bp)

@bp.route('/')
def test_for_vue():
    return render_template('index.html')

parser = reqparse.RequestParser()

class Project(Resource):
    def get(self, id):
        project = Project.abort_if_project_doesnt_exist(id)
        return project.attributes

    def delete(self):
        pass

    def put(self):
        pass

    @staticmethod
    def abort_if_project_doesnt_exist(id):
        try:
            project = g.gl.projects.get(id)
        except gitlab.GitlabGetError as e:
            abort(100404, message="Project %s doesn't exist" % id)
        return project
        # @TODOS
        # project = Project.query.filter_by(id=project_id).first()
        # if project is None:
        #     abort(404, message="Project %s doesn't exist" % project_id)


class ProjectList(Resource):
    def get(self):
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        # projects = Project.query.limit(10).offset(10)
        projects = g.gl.projects.list(all=True)
        res = {}
        res['projects'] = [{
            'id': p.id,
            'name': p.name,
            'ssh_url_to_repo': p.ssh_url_to_repo,
            'owner': p.owner['name'],
            'web_url': p.web_url,
            'visibility': p.visibility
        } for p in projects]
        res['total'] = len(projects)
        return res

    def post(self):
        parser.add_argument('id', help='ID require int')
        args = parser.parse_args()
        return args['id']


class Branch(Resource):
    def patch(self, id):
        parser.add_argument('project_id', help='ID require int')
        parser.add_argument('operation', help='Operation required')
        args = parser.parse_args()
        project_id = args['project_id']
        operation = args['operation']
        # 项目
        project = Project.abort_if_project_doesnt_exist(project_id)
        # 分支
        branch = project.branches.get(id)
        if operation == 'protect':
            branch.protect()
            return '已锁定'
        elif operation == 'unprotect':
            branch.unprotect()
            return '已解锁'



class BranchList(Resource):
    def get(self):
        project_id = request.args.get('project_id')
        project = Project.abort_if_project_doesnt_exist(project_id)
        return [b.get_id() for b in project.branches.list()]


api.add_resource(Project, '/projects/<int:id>', endpoint='project')
api.add_resource(ProjectList, '/projects', endpoint='projects')
api.add_resource(Branch, '/branches/<string:id>', endpoint='branch')
api.add_resource(BranchList, '/branches', endpoint='branches')