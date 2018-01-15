from flask import Blueprint, g, current_app
from flask_restful import Api, Resource, reqparse
from flask_socketio import emit

from app import socketio, redis
from models.projects import Project as ProjectModel
from models.hosts import Host as HostModel
from models.users import User as UserModel
from models.deploys import Deploy as DeployModel
from models.deploylogs import DeployLog as LogModel
from libs.services import DeployService

import time
from threading import Lock

bp = Blueprint('deploy', __name__)
api = Api(bp)

thread = None
thread_lock = Lock()

channel = 'deploy'
pubsub = redis.pubsub()


def background_thread(channel):
    pubsub.subscribe(channel)
    for msg in pubsub.listen():
        if msg['type'] == 'message':
            socketio.emit(
                'my_response', {'data': msg['data'].decode('utf-8')},
                namespace='/ws/deploy_results')


@socketio.on('connect', namespace='/ws/deploy_results')
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread, channel)
    emit('my_response', {'data': 'Welcome'})


@socketio.on('my_event', namespace='/ws/deploy_results')
def send_message(msg):
    emit('my_response', {'data': msg['data']})


# @socketio.on('my_broadcast_event', namespace='/ws/deploy_results')
# def send_broadcast_message(message):
#     emit(
#         'my_response', {'data': 'Welcome ' + g.current_user.username},
#         broadcast=True)

# @socketio.on('disconnect', namespace='/ws/deploy_results')
# def disconnect():
#     # 画蛇添足喝不到酒
#     pubsub.unsubscribe(channel)
#     print('Client disconnected')

parser = reqparse.RequestParser()


class Deploy(Resource):
    def get(self, id):
        emit('my_response', {'data': 'deploy test'})
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
        parser.add_argument('service', help='required')
        parser.add_argument('version_intro', help='required')
        parser.add_argument('commit', action='append', help='required')
        args = parser.parse_args()

        project_id = int(args['project_id'])
        branch_id = args['commit'][0]
        commit_id = args['commit'][1]
        user_id = int(args['current_user'])
        environment = int(args['env'])
        service = True if args['service'] == 'True' else False

        _project = g.gl.projects.get(project_id)
        project_args = {
            'name': _project.attributes.get('name'),
            'repo_ssh_url': _project.attributes.get('ssh_url_to_repo'),
            'service': service
        }
        deploy = DeployModel.query.filter(
            DeployModel.project_id == project_id, DeployModel.status != 5,
            DeployModel.env == environment).first()
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
        config = current_app.config['DEPLOYMENT']
        ds = DeployService(deploy, config, project_args)
        ds.run()
        return '部署请求已发出，稍后请查收消息'


class DeployLog(Resource):
    def patch(self, id):
        # parser.add_argument('lid', help='lid required')
        # args = parser.parse_args()
        # id = args['lid']
        log = LogModel.get(id)
        LogModel.update(log, readed=1)
        return 'updated'


class DeployLogList(Resource):
    def get(self):
        logs = LogModel.find(
            readed=0, user_id=g.current_user.attributes.get('id'))
        return [{'id': l.id, 'msg': l.log} for l in logs]


api.add_resource(Deploy, '/deploys/<int:id>', endpoint='deploy')
api.add_resource(DeployList, '/deploys', endpoint='deploys')
api.add_resource(DeployLog, '/logs/<int:id>', endpoint='log')
api.add_resource(DeployLogList, '/logs', endpoint='logs')
