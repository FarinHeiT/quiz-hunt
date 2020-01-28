class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Maindb.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'topsecret'
    SECURITY_LOGIN_URL = '/auth/login'
    UPLOAD_FOLDER = 'files'
    # Size in bytes
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
