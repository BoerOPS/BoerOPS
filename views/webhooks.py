import json

from flask import Blueprint, render_template, request

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

    commits = [(item['id'], item['message'], item['url'], item['timestamp']) for item in body['commits']]
    print(project_name)
    print(ref)
    print(user_name)
    print(commits)
    return ''