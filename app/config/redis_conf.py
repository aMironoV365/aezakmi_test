from redis.asyncio import Redis
from app.config.config import settings

redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_redis() -> Redis:
    return redis
