import os

class Configuration(object):
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG = True
    SECRET_KEY = 'python head'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/nsp.db' % APPLICATION_DIR
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# class Configuration(object):
#     DEBUG = True
#     MYSQL_HOST = 'localhost'
#     MYSQL_USER = 'root'
#     MYSQL_PASSWORD = ''
#     MYSQL_DB = 'nsp'
#     MYSQL_UNIX_SOCKET = '/opt/lampp/var/mysql/mysql.sock'
#     MYSQL_CURSORCLASS = 'DictCursor'
