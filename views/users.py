from flask import Blueprint, redirect, request, jsonify
from flask_restful import Api, Resource, url_for
import requests

from app import redis

bp = Blueprint('user', __name__)
api = Api(bp)


client_id = '8d3b6063c3810d8ba1698d44c96454a767232f33a8e6fa23110905310ec4d768'
secert = '381e4e76b806ddad32f51c238386d1a0ba80fa211b48bf542c6a101cbf44a48f'
redirect_uri = 'http://webhook.mail.heclouds.com/oauth2/welcome'


@bp.route('/oauth2/welcome')
def oauth2_welcome():
    code = request.args.get('code')
    # parameters = 'client_id=APP_ID&client_secret=APP_SECRET&code=RETURNED_CODE&grant_type=authorization_code&redirect_uri=REDIRECT_URI'
    # RestClient.post 'http://gitlab.example.com/oauth/token', parameters
    parameters = {
        'client_id': client_id,
        'client_secret': secert,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }
    url = 'http://gitlab.onenet.com/oauth/token'
    resp = requests.post(url, params=parameters)
    resp = resp.json()
    access_token = resp.get('access_token')
    created_at = resp.get('expires_in')
    refresh_token = resp.get('refresh_token')
    scope = resp.get('scope')
    token_type = resp.get('token_type')
    redis.set('access_token', access_token)
    redis.set('refresh_token', refresh_token)
    redis.set('scope', scope)
    redis.set('token_type', token_type)
    return jsonify(resp)


@bp.route('/auth/login')
def auth_login():
    # https://gitlab.example.com/oauth/authorize?client_id=APP_ID&redirect_uri=REDIRECT_URI&response_type=code&state=YOUR_UNIQUE_STATE_HASH
    state = 'gitlab'
    url = 'http://gitlab.onenet.com/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code&state=%s' % (client_id, redirect_uri, state)
    return redirect(url)


@bp.route('/user/token')
def get_user_token():
    access_token = redis.get('access_token')
    if access_token is None:
        return redirect('/auth/login')
    import gitlab
    gl = gitlab.Gitlab('http://gitlab.onenet.com', oauth_token=access_token, api_version='4')
    
    project = gl.projects.get(8)
    # return 'access_token: %s' % access_token
    return project.name


class User(Resource):
    def get(self, id):
        return {'task': 'done'}

api.add_resource(User, '/user/<int:id>')