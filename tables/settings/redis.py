from .base import *

redis_host = os.environ.get('REDIS_HOST', 'localhost')


CHANNEL_LAYERS = {
    "default": {

        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(redis_host, 6379)],
        },
        "ROUTING": "tables.routing.channel_routing",
    },
}
