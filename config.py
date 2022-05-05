class BaseConfig(object):
    DB = "mysql://root:root@localhost/flask_admin?charset=utf8mb4"
    REDIS_TYPE = "socket"
    REDIS_HOST = ""
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_SOCKET = "/tmp/reids.sock"
    TOKEN_EXPIRY = 720000


class ProductConfig(BaseConfig):
    NAME = "hi"
