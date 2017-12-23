from flask import Blueprint, render_template, request, jsonify, g
from flask_restful import Api, Resource, reqparse, abort
import gitlab

from models.commits import Commit as CommitModel

import json

bp = Blueprint('webhook', __name__)
api = Api(bp)

parser = reqparse.RequestParser()

def abort_if_user_doesnt_exist(username):
    try:
        _user = g.gl.users.list(username=username)[0]
    except IndexError as e:
        abort(404, message="User %s doesn't exist" % username)
    return _user

class WebHook(Resource):
    def get(self, username):
        _user = abort_if_user_doesnt_exist(username)
        return {'id': _user.id, 'name': _user.name, 'email': _user.email}

    def delete(self, username):
        _user = abort_if_user_doesnt_exist(username)
        _user.delete()
        return '删除用户成功'

class WebHookList(Resource):
    def get(self):
        pass

    def post(self):
        parser.add_argument('name', help='required')
        parser.add_argument('email', help='required')
        parser.add_argument('username', help='required')
        parser.add_argument('password', help='required')
        args = parser.parse_args()
        try:
            user = g.gl.users.create({
                'email': args['email'],
                'password': args['password'],
                'username': args['username'],
                'name': args['name']
            })
        except gitlab.exceptions.GitlabCreateError as e:
            return 'create error'
        onenet_v3 = g.gl.projects.get(32)
        public_doc = g.gl.projects.get(9)
        onenet_v3.members.create({
            'user_id': user.id,
            'access_level': gitlab.DEVELOPER_ACCESS
        })
        public_doc.members.create({
            'user_id': user.id,
            'access_level': gitlab.DEVELOPER_ACCESS
        })
        return 'create done'


api.add_resource(WebHook, '/webhooks/<string:username>', endpoint='webhook')
api.add_resource(WebHookList, '/webhooks', endpoint='webhooks')

hook_url = 'http://webhook.mail.heclouds.com/pushhook'
gl = gitlab.Gitlab('http://gitlab.onenet.com', 'W8jWv6i_X9WRtMRr2xgv')


# 添加
@bp.route('/script/add_pushhook')
def add_pushhook():
    res_success = res_already = []
    for p in gl.projects.list(all=True):
        per_project_hooks = [
            hook.url for hook in gl.project_hooks.list(project_id=p.id)
        ]
        if hook_url not in per_project_hooks:
            gl.project_hooks.create(
                {
                    'url': hook_url,
                    'push_events': 1,
                    'enable_ssl_verification': 0
                },
                project_id=p.id)
            res_success.append(p.name)
        else:
            res_already.append(p.name)
    return jsonify(res_success, res_already)


# 删除
@bp.route('/script/del_pushhook')
def del_pushhook():
    res_success = res_nohas = []
    for p in gl.projects.list(all=True):
        for hook in gl.project_hooks.list(project_id=p.id):
            if hook.url == hook_url:
                hook.delete()
                res_success.append(p.name)
            else:
                res_nohas.append(p.name)
    return jsonify(res_success, res_nohas)


@bp.route('/pushhook', methods=['POST'])
def push_hook():
    event = request.headers.get('X-Gitlab-Event')
    if event is None and event != 'Push Hook':
        return '', 404

    body = json.loads(request.data.decode('utf-8'), encoding='utf-8')
    project_id = body['project_id']
    project_name = body['project']['name']

    ref = body['ref'].split('/')[-1]

    user_id = body['user_id']
    user_username = body['user_username']
    user_name = body['user_name']
    user_email = body['user_email']

    commits = ((item['id'], item['message'], item['url'], item['timestamp'])
               for item in body['commits'])
    for c in commits:
        CommitModel.create(
            project_id=project_id,
            project_name=project_name,
            ref=ref,
            commit_id=c[0],
            commit_msg=c[1],
            commit_url=c[2],
            commit_timestamp=c[3],
            user_id=user_id,
            user_username=user_username,
            user_name=user_name,
            user_email=user_email)
    return ''
