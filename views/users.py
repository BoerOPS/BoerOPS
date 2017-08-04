from flask import Blueprint, redirect, request, jsonify
from flask_restful import Api, Resource, url_for
import requests

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
    r = requests.post(url, params=parameters)
    return jsonify(r.json())


@bp.route('/auth/login')
def auth_login():
    # https://gitlab.example.com/oauth/authorize?client_id=APP_ID&redirect_uri=REDIRECT_URI&response_type=code&state=YOUR_UNIQUE_STATE_HASH
    state = 'gitlab'
    url = 'http://gitlab.onenet.com/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code&state=%s' % (client_id, redirect_uri, state)
    return redirect(url)


class User(Resource):
    def get(self, id):
        return {'task': 'done'}

api.add_resource(User, '/user/<int:id>')