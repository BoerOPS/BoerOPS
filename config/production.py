from . import Config

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://boer:123456@mysql/deploy_ops_dev'

