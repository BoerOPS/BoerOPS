import socket

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_mail import Mail
import redis

from config import config

db = SQLAlchemy()
mail = Mail()
# redis = redis.Redis(host='127.0.0.1', port=6379, db=0)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)

    from views.deploys import bp as deploy_bp
    from views.projects import bp as project_bp
    from views.users import bp as user_bp
    app.register_blueprint(deploy_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(user_bp)

    return app

if socket.gethostname() in ['Boer-PC', 'boer-PC']:
    app = create_app('dev')
else:
    app = create_app('prod')