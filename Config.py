import os
basedir = os.path.abspath(os.path.dirname(__file__))


# 基类
class Config:
    SECRET_KEY = 'webProject'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flask]'
    FLASKY_MAIL_SENDER = 'Flask Admin'
    FLASKY_ADMIN = ['16130120129']
    @staticmethod
    def init_app(app):
        pass


# 开发环境
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@39.105.64.7:3306/webProject'
    REDIS_URL = "redis://:@39.105.64.7:6379/1"

# 测试环境
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/webProject'
    REDIS_URL = "redis://:123456@localhost:6379/1"


# 生产环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/webProject'


# 设置一个config 字典中,注册了不同的配置环境
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
