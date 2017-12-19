from flask import Blueprint, request
from flask_restful import Api, Resource, url_for, reqparse

from models.hosts import Host as Host_Model

bp = Blueprint('host', __name__)
api = Api(bp)

parser = reqparse.RequestParser()


class Host(Resource):
    def get(self, id):
        return {'task': 'done'}


class HostList(Resource):
    def get(self):
        env = request.args.get('env')
        print('-env->', env)
        if env:
            _hosts = Host_Model.find(env=env)
            print(_hosts)
            print('---hosts--->', [h.ip_addr for h in _hosts])
            return [h.ip_addr for h in _hosts]
        res = {}
        _hosts = Host_Model.all()
        res['hosts'] = [{
            'id': h.id,
            'ip_addr': h.ip_addr,
            'env': h.env
        } for h in _hosts]
        res['total'] = len(_hosts)
        return res

    def post(self):
        parser.add_argument('ip_addr', help='ip_addr required')
        parser.add_argument('env', help='env required')
        args = parser.parse_args()
        ip_addr = args['ip_addr']
        env = args['env']
        if env == 'True':
            env = 0
        else:
            env = 1
        _h = Host_Model.first(ip_addr=ip_addr)
        if _h is not None:
            return '主机已经存在'
        Host_Model.create(ip_addr=ip_addr, env=env)
        return '添加成功'


api.add_resource(Host, '/hosts/<int:id>', endpoint='host')
api.add_resource(HostList, '/hosts', endpoint='hosts')