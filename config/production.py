from . import Config

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@mysql/boerops_dev'

