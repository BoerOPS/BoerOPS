from flask import Blueprint, render_template, request, g
from flask_restful import Api, Resource, abort, reqparse

import gitlab
from models.projects import Project as ProjectModel
from models.hosts import Host as HostModel

bp = Blueprint('project', __name__)
api = Api(bp)


@bp.route('/')
def test_for_vue():
    return render_template('index.html')


parser = reqparse.RequestParser()


class Project(Resource):
    def get(self, id):
        project = abort_if_project_doesnt_exist(id)
        return project.attributes

    def delete(self):
        pass

    def put(self):
        pass


def abort_if_project_doesnt_exist(id):
    try:
        _project = g.gl.projects.get(id)
    except gitlab.GitlabGetError as e:
        abort(404, message="Project %s doesn't exist" % id)
    return _project


class ProjectList(Resource):
    def get(self):
        ops = request.args.get('ops')
        # projects = ProjectModel.query.limit(10).offset(10)
        # https://gitlab.com/help/api/projects.md
        projects = g.gl.projects.list(membership=True)
        if g.current_user.attributes.get('is_admin'):
            projects = g.gl.projects.list(all=True)
        if ops is not None:
            membership_projects = [p.id for p in projects]
            _projects = []
            for pid in membership_projects:
                _p = ProjectModel.get(int(pid))
                if _p is None:
                    continue
                _projects.append(_p)
            # _projects = [
            #     ProjectModel.get(pid) for pid in membership_projects
            #     if ProjectModel.get(pid) is not None
            # ]
            return [{
                'project_id': p.id,
                'name': p.name
            } for p in _projects]
        res = {
            'projects': [{
                'id': p.id,
                'name': p.name,
                'ssh_url_to_repo': p.ssh_url_to_repo,
                'owner': p.owner['name'],
                'web_url': p.web_url,
                'visibility': p.visibility
            } for p in projects],
            'total':
            len(projects)
        }
        return res

    def post(self):
        parser.add_argument('name', help='required')
        parser.add_argument('beforeCmd', help='required')
        parser.add_argument('afterCmd', help='required')
        parser.add_argument('hosts', action='append', help='required')
        parser.add_argument('project_id', help='required')
        args = parser.parse_args()
        _project = ProjectModel.get(args['project_id'])
        if _project is not None:
            return '项目已存在，请勿重复创建！'
        hosts = [HostModel.get(int(h)) for h in args['hosts']]
        _project = ProjectModel.create(
            id=args['project_id'],
            name=args['name'],
            before_cmd=args['beforeCmd'],
            after_cmd=args['afterCmd'],
            hosts=hosts)
        if _project is None:
            return '创建失败'
        return '新建成功'


class Branch(Resource):
    def patch(self, id):
        parser.add_argument('project_id', help='ID require int')
        parser.add_argument('operation', help='Operation required')
        args = parser.parse_args()
        project_id = args['project_id']
        operation = args['operation']
        # 项目
        project = abort_if_project_doesnt_exist(project_id)
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
        project = abort_if_project_doesnt_exist(project_id)
        return [b.get_id() for b in project.branches.list(all=True)]


class CommitList(Resource):
    def get(self):
        project_id = request.args.get('project_id')
        project = abort_if_project_doesnt_exist(project_id)
        res = []
        for branch in [b.get_id() for b in project.branches.list(all=True)]:
            pre_branch_commits = {'value': branch, 'label': branch}
            commits = project.commits.list(ref_name=branch)
            pre_branch_commits['children'] = [
                dict(
                    value=c.attributes['id'],
                    label=c.attributes['author_name'] + ' $ ' +
                    c.attributes['message'] + ' @ ' + c.attributes['short_id'])
                for c in commits
            ]
            res.append(pre_branch_commits)
        return res


api.add_resource(Project, '/projects/<int:id>', endpoint='project')
api.add_resource(ProjectList, '/projects', endpoint='projects')
api.add_resource(Branch, '/branches/<string:id>', endpoint='branch')
api.add_resource(BranchList, '/branches', endpoint='branches')
api.add_resource(CommitList, '/commits', endpoint='commits')
