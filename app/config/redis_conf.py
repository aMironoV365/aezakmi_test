from redis.asyncio import Redis
from app.config.config import settings


redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_redis() -> Redis:
    """
    Получить подключение к Redis.

    Эта функция возвращает уже установленное подключение к Redis,
    которое было инициализировано с использованием URL из настроек.

    Возвращаемое значение:
        Redis: объект для работы с Redis через Redis.asyncio.
    """
    return redis
