import socket

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
from flask_restful import Api
from flask_socketio import SocketIO
from flask_mail import Mail
import redis

from config import config

db = SQLAlchemy()
async_mode = None
socketio = SocketIO()
mail = Mail()
# lm = LoginManager()
# lm.login_view = '/user/login'

pool = redis.ConnectionPool(host='172.19.3.165', port=6379, db=1)
redis = redis.Redis(connection_pool=pool)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    # lm.init_app(app)
    mail.init_app(app)
    socketio.init_app(app, async_mode=async_mode)

    from views.deploys import bp as deploy_bp
    from views.projects import bp as project_bp
    from views.users import bp as user_bp
    from views.webhooks import bp as webhook_bp
    from views.hosts import bp as host_bp
    app.register_blueprint(deploy_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(webhook_bp)
    app.register_blueprint(host_bp)

    return socketio, app


# from models.users import User
# @lm.user_loader
# def load_user(id):
#     return User.query.get(int(id))

if socket.gethostname() in ['Boer-PC', 'boer-PC', 'Cloud_public_node01']:
    socketio, app = create_app('dev')
else:
    socketio, app = create_app('prod')
