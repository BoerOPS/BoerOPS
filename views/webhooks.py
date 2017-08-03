import json

from flask import Blueprint, render_template, request

from models.commits import Commit
from models.tests import Test

bp = Blueprint('webhook', __name__)


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
        Commit.create(
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


@bp.route('/orm_test/<name>')
def orm_test(name):
    Test.create(name=name)
    return 'done'