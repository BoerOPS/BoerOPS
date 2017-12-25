from . import Config

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1/deploy_ops_dev'
    CHECKOUT_PATH = 'E:/tmp'
    DEPLOY_PATH = 'E:/tmp/deploy'
