from . import Config

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://boer:123456@172.19.3.165/deploy_ops_dev'
    DEPLOYMENT = {
        'CHECKOUT_PATH': '/tmp',
        'DEPLOY_PATH': '/tmp/deploy',
        'CODE_USER': 'apache',
        'CODE_GROUP': 'apache'
    }
