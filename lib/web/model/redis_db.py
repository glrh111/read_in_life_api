
from functools import wraps
import redis as _redis
from lib.serve.config import app_config

redis = _redis.StrictRedis(**app_config.REDIS_CONFIG)

def R(namespace):
    """use like this
       ('session')('wocao') : key = 'session:wocao'
    """
    def wrapper(id):
        return '{}:{}'.format(namespace, id)
    return wrapper


if __name__ == '__main__':
    print