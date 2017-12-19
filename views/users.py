from flask import Blueprint, redirect, request, jsonify, make_response, current_app, g
# from flask_login import login_user, logout_user
from flask_restful import Api, Resource, url_for
import requests
import gitlab

# from app import redis
from models.users import User

from functools import wraps
from urllib.parse import urlencode


# @bp.before_app_request
def allow_cross_domain(f):
    @wraps(f)
    def set_resp_headers(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    return set_resp_headers


bp = Blueprint('user', __name__)
api = Api(bp)

client_id = '8d3b6063c3810d8ba1698d44c96454a767232f33a8e6fa23110905310ec4d768'
secert = '381e4e76b806ddad32f51c238386d1a0ba80fa211b48bf542c6a101cbf44a48f'
redirect_uri = 'http://webhook.mail.heclouds.com/oauth2/welcome'


@bp.route('/oauth2/welcome')
@allow_cross_domain
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
    print('--resp-->', resp)
    access_token = resp.get('access_token')
    created_at = resp.get('created_at')
    refresh_token = resp.get('refresh_token')
    scope = resp.get('scope')
    token_type = resp.get('token_type')
    print('--access_token-->', access_token)
    # 入库操作
    if access_token:
        gl = gitlab.Gitlab(
            'http://gitlab.onenet.com',
            oauth_token=access_token,
            api_version='4')
        gl.auth()
        u = User.first(gitlab_id=gl.user.id)
        if u is None:
            u = User.create(
                gitlab_id=gl.user.id,
                gitlab_username=gl.user.username,
                gitlab_name=gl.user.name,
                gitlab_email=gl.user.email,
                gitlab_avatar=gl.user.avatar_url)
    else:
        return jsonify(resp)
        # {
        #     'error': 'invalid_grant',
        #     'error_description': 'The provided authorization grant is invalid, expired, revoked, does not match the redirection URI used in the authorization request, or was issued to another client.'
        # }
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
@allow_cross_domain
def auth_login():
    # https://gitlab.example.com/oauth/authorize?client_id=APP_ID&redirect_uri=REDIRECT_URI&response_type=code&state=YOUR_UNIQUE_STATE_HASH
    state = 'gitlab'
    url = 'http://gitlab.onenet.com/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code&state=%s' % (
        client_id, redirect_uri, state)
    return redirect(url)


@bp.route('/user/token')
def get_user_token():
    print('-----request.cookies------->', request.cookies)
    if not request.cookies.get('access_token'):
        if not request.cookies.get('refresh_token'):
            return redirect('/auth/login')
        return redirect('/oauth2/welcome')
    import gitlab
    gl = gitlab.Gitlab(
        'http://gitlab.onenet.com',
        oauth_token=request.cookies.get('access_token'),
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
    g.current_user = _user
    # login_user(_user)
    resp = make_response(redirect('/'))
    print('--<<<token', g.current_user.generate_auth_token(expires=3600))
    resp.set_cookie('token', g.current_user.generate_auth_token(expires=3600))
    return resp
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
    # logout_user()
    resp = make_response(redirect('/'))
    resp.set_cookie('access_token', '')
    resp.set_cookie('token', '')
    return resp


@bp.before_app_request
def before_pre_request():
    if request.path in [
            '/user/login', '/user/token', '/auth/login', '/oauth2/welcome'
    ]:
        return
    token = request.headers.get('TOKEN')
    if not token:
        return jsonify('Authorization error'), 403
    gl = gitlab.Gitlab(
        'http://gitlab.onenet.com', oauth_token=token, api_version='4')
    gl.auth()
    g.current_user = gl.user
    g.gl = gl

# from flask import g

# def add_resp_headers(f):
#     if not hasattr(g, 'request_callbacks'):
#         g.request_callbacks = []
#     g.request_callbacks.append(f)
#     return f

# return resp

class CurrentUser(Resource):
    def get(self):
        return g.current_user.attributes


api.add_resource(CurrentUser, '/currentuser', endpoint='currentuser')
