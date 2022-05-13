import os


class BaseConfig(object):
    DB = "mysql://root:root@localhost/flask_admin?charset=utf8mb4"
    DB_POOL_SIZE = 10
    REDIS_TYPE = "socket"
    REDIS_HOST = ""
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_SOCKET = "/tmp/redis.sock"
    TOKEN_EXPIRY = 720000
    UP_PATH = os.getcwd() + "/static/files/"
    UP_URL = "/static/files/"


class ProductConfig(BaseConfig):
    NAME = "hi"
