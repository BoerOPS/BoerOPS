from flask import Blueprint, redirect, request, jsonify, session
from flask_login import login_user, logout_user
from flask_restful import Api, Resource, url_for
import requests

from app import redis
from models.users import User

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
    # refresh token
    if code is None:
        print('----------> refresh token')
        parameters = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'scope': session['scope']
        }
    url = 'http://gitlab.onenet.com/oauth/token'
    resp = requests.post(url, params=parameters)
    resp = resp.json()
    access_token = resp.get('access_token')
    created_at = resp.get('expires_in')
    refresh_token = resp.get('refresh_token')
    scope = resp.get('scope')
    token_type = resp.get('token_type')
    # redis.set('access_token', access_token, ex=7000)
    # redis.set('refresh_token', refresh_token)
    # redis.set('scope', scope)
    # redis.set('token_type', token_type)
    session['access_token'] = access_token
    session['refresh_token'] = refresh_token
    session['created_at'] = created_at
    session['scope'] = scope
    session['token_type'] = token_type
    print(resp)
    # return jsonify(resp)
    return redirect('/user/token')


@bp.route('/auth/login')
def auth_login():
    # https://gitlab.example.com/oauth/authorize?client_id=APP_ID&redirect_uri=REDIRECT_URI&response_type=code&state=YOUR_UNIQUE_STATE_HASH
    state = 'gitlab'
    url = 'http://gitlab.onenet.com/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code&state=%s' % (
        client_id, redirect_uri, state)
    return redirect(url)


@bp.route('/user/token')
def get_user_token():
    if session.get('access_token') is None:
        if session.get('refresh_token') is None:
            return redirect('/auth/login')
        return redirect('/oauth2/welcome')
    import gitlab
    gl = gitlab.Gitlab(
        'http://gitlab.onenet.com',
        oauth_token=session.get('access_token'),
        api_version='4')
    gl.auth()
    current_user = gl.user
    _user = User.query.filter_by(gitlab_id=current_user.id).first()
    if _user is None:
        _user = User.create(
            gitlab_id=current_user.id,
            gitlab_username=current_user.username,
            gitlab_name=current_user.name,
            gitlab_email=current_user.email,
            gitlab_avatar=current_user.avatar_url)
    login_user(_user)
    return redirect('/')
    # project = gl.projects.get(29)
    # commits = project.commits.list()
    # projects = gl.projects.list(all=True)
    # branches = project.branches.list()
    # users = gl.users.list(all=True)
    # return jsonify(
    #     name=name or project.name,
    #     branches=', '.join([b.name for b in branches]),
    #     projects=', '.join([p.name for p in projects]),
    #     total_projects=len(projects),
    #     users=', '.join([u.username for u in users]),
    #     total_users=len(users),
    #     whoami=current_user.name)
    # return redirect('/')
    return jsonify(
        id=current_user.id,
        username=current_user.username,
        name=current_user.name,
        email=current_user.email,
        avatar=current_user.avatar_url)

@bp.route('/user/login')
def login():
    return '<h3><a href="/user/token">Gitlab Login</a></h3>'

@bp.route('/user/logout')
def logout():
    logout_user()
    session.pop('access_token')
    return redirect('/')


# class User(Resource):
#     def get(self, id):
#         return {'task': 'done'}

# api.add_resource(User, '/user/<int:id>')
