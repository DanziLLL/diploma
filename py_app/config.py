class Config(object):
    MD5_SALT = 'P@ssw0rd42!'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'P@ssw0rd'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 120,
        'pool_pre_ping': True
    }