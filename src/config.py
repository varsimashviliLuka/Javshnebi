from decouple import config
from os import path, sep, pardir
from datetime import timedelta

class Config(object):
    # Base config
    SECRET_KEY = config('SECRET_KEY','secret_key')

    BASE_DIR = path.abspath(path.dirname(__file__) + sep + pardir)
    TEMPLATES_FOLDERS = 'src/templates'

    # Mysql config
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MYSQL_DATABASE = config('MYSQL_DATABASE', 'default_database')
    MYSQL_USER = config('MYSQL_USER', 'default_user')
    MYSQL_PASSWORD = config('MYSQL_PASSWORD', 'default_password')
    MYSQL_HOST = config('MYSQL_HOST','MYSQL_HOST')
    MYSQL_ROOT_PASSWORD = config('MYSQL_ROOT_PASSWORD','MYSQL_ROOT_PASSWORD')
    # MySQL connection URI
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'

    # JWT token config
    JWT_SECRET_KEY = config('JWT_SECRET_KEY', 'default_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=12)
    AUTHORIZATION ={
        'JsonWebToken': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }

    # Mail config

    MAIL_SERVER= config('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = config('MAIL_PORT', 587)
    MAIL_USERNAME = config('MAIL_USERNAME', 'MAIL_USERNAME')
    MAIL_PASSWORD = config('MAIL_PASSWORD', 'MAIL_PASSWORD')


class DevConfig(Config):
    TESTING = True

    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}/{Config.MYSQL_DATABASE}'
    )


