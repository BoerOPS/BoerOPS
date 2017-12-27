from flask import Blueprint, redirect, request, jsonify, make_response, current_app, g
from flask_restful import Api, Resource
import requests
import gitlab

from models.users import User as UserModel

from urllib.parse import urlencode

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
    # access token parameters
    parameters = {
        'client_id': client_id,
        'client_secret': secert,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }
    # refresh token parameters
    if code is None:
        parameters = {
            'grant_type': 'refresh_token',
            'refresh_token': request.args.get('refresh_token'),
            'scope': request.args.get('scope')
        }
    url = 'http://gitlab.onenet.com/oauth/token'
    resp = requests.post(url, data=parameters)
    resp = resp.json()
    access_token = resp.get('access_token')
    created_at = resp.get('created_at')
    refresh_token = resp.get('refresh_token')
    scope = resp.get('scope')
    token_type = resp.get('token_type')
    # 入库操作
    if access_token:
        print('---access_token--->', access_token)
        gl = gitlab.Gitlab(
            'http://gitlab.onenet.com',
            oauth_token=access_token,
            api_version='4')
        gl.auth()
        u = UserModel.get(gl.user.id)
        if u is None:
            u = UserModel.create(
                id=gl.user.id,
                gitlab_username=gl.user.username,
                gitlab_name=gl.user.name,
                gitlab_email=gl.user.email,
                gitlab_avatar=gl.user.avatar_url)
    else:
        return jsonify(resp)
    # refresh token return
    if code is None:
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'created_at': created_at,
            'scope': scope,
            'token_type': token_type
        })
    # access token return
    querystring = urlencode({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'created_at': created_at,
        'scope': scope,
        'token_type': token_type
    })
    return redirect('http://boer.mail.heclouds.com/#/login?' + querystring)
    # return redirect('http://127.0.0.1:8080/#/login?' + querystring)


@bp.route('/auth/login')
def auth_login():
    # https://gitlab.example.com/oauth/authorize?client_id=APP_ID&redirect_uri=REDIRECT_URI&response_type=code&state=YOUR_UNIQUE_STATE_HASH
    state = 'gitlab'
    url = 'http://gitlab.onenet.com/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code&state=%s' % (
        client_id, redirect_uri, state)
    return redirect(url)


@bp.before_app_request
def before_pre_request():
    if request.path in ['/auth/login', '/oauth2/welcome']:
        return
    token = request.headers.get('TOKEN')
    if not token:
        return jsonify('Authorization error'), 403
    gl = gitlab.Gitlab(
        'http://gitlab.onenet.com', oauth_token=token, api_version='4')
    gl.auth()
    g.current_user = gl.user
    g.gl = gl


@bp.route('/joke')
def joke():
    from pyquery import PyQuery as pq
    from random import randint
    doc = pq('http://xiaohua.zol.com.cn/new/')
    jokes = [doc(i).text() for i in doc('div.summary-text')]
    return jsonify(code=100200, joke=jokes[randint(0, len(jokes))])


class CurrentUser(Resource):
    def get(self):
        return g.current_user.attributes


api.add_resource(CurrentUser, '/currentuser', endpoint='currentuser')
