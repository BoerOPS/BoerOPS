from flask import Blueprint, render_template, request, jsonify
# from flask_login import login_required
from flask_restful import Api, Resource, url_for

import gitlab

bp = Blueprint('project', __name__)
api = Api(bp)

@bp.route('/')
def test_for_vue():
    return render_template('index.html')


@bp.route('/projects')
def get_all_projects():
    access_token = request.args.get('access_token')
    gl = gitlab.Gitlab(
        'http://gitlab.onenet.com', oauth_token=access_token, api_version='4')
    projects = gl.projects.list(all=True)
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
    return jsonify(res)


class Project(Resource):
    def get(self, id):
        projects = g.gl.projects.all()
        res = { p.name: p.name for p in projects}
        return res

    def post(self):
        pass

    def put(self):
        pass


api.add_resource(Project, '/projects/<int:id>')