import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(
    #     os.path.dirname(__file__),
    #     'static',
    # ),
    os.path.join(BASE_DIR, "static"),
)

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        # 'OPTIONS': {
        #     'DB': 1,
        #     'PASSWORD': 'yadayada',
        #     'PARSER_CLASS': 'redis.connection.HiredisParser',
        #     'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
        #     'CONNECTION_POOL_CLASS_KWARGS': {
        #         'max_connections': 50,
        #         'timeout': 20,
        #     }
        # },
    },
}