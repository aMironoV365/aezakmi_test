import aioredis
from functools import lru_cache
from app.config.config import settings

@lru_cache
def get_redis_url():
    return settings.REDIS_URL

redis = None

async def get_redis():
    global redis
    if not redis:
        redis = await aioredis.from_url(get_redis_url(), encoding="utf8", decode_responses=True)
    return redis