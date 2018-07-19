import os

basedir = os.path.abspath (os.path.dirname (__file__))


class Config (object):
    DEBUG = True
    SECRET_KEY = 'sfasgfakljrhgsfgk'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join (basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = False
