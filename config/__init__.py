import os
bashdir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(bashdir, 'BoerOPS.db')

    @staticmethod
    def init_app(app):
        pass

from config.development import DevelopmentConfig
from config.production import ProductionConfig

config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig
}
