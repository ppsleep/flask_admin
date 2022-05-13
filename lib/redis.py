import redis


class Redis():
    def __init__(self, config):
        self.__config = config
        if config["REDIS_TYPE"] == "socket":
            self.__redis = redis.Redis(
                unix_socket_path=config["REDIS_SOCKET"],
                db=config["REDIS_DB"]
            )
        else:
            self.__redis = redis.Redis(
                host=config["REDIS_HOST"],
                port=config["REDIS_PORT"],
                db=config["REDIS_DB"]
            )

    def config(self, key):
        return self.__config[key]

    def set(self, key, value):
        return self.__redis.set(key, value)

    def setex(self, key, time, value):
        return self.__redis.setex(key, time, value)

    def get(self, key):
        return self.__redis.get(key)

    def delete(self, key):
        return self.__redis.delete(key)
