import redis
from ..config import settings

def get_redis_client():
    """
    Connects to the Redis database using the provided REDIS_URL from the environment.
    """
    return redis.StrictRedis.from_url(settings.redis_url, decode_responses=True)
