from . import Config

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://boer:123456@172.19.3.165/deploy_ops_dev'
    DEPLOYMENT = {
        'CHECKOUT_PATH': 'E:\\tmp',
        'DEPLOY_PATH': 'E:\\tmp\\deploy',
        'CODE_USER': 'www',
        'CODE_GROUP': 'www'
    }
