import aioredis
from functools import lru_cache
from app.config.config import settings


@lru_cache
def get_redis_url():
    """
    Функция для получения URL для подключения к Redis.

    Используется кэширование (LRU), чтобы избежать повторного чтения URL из настроек
    при многократных вызовах. Считывает URL из конфигурационного файла.

    Возвращает:
        str: URL для подключения к Redis.
    """
    return settings.REDIS_URL


# Глобальная переменная для хранения подключения к Redis
redis = None


async def get_redis():
    """
    Асинхронная функция для получения экземпляра клиента Redis.

    Если подключение к Redis еще не установлено, оно создается при первом вызове этой функции.
    Для последующих вызовов будет использоваться сохраненное подключение, чтобы избежать
    избыточных подключений.

    Возвращает:
        aioredis.Redis: Экземпляр клиента Redis.
    """
    global redis
    if not redis:
        redis = await aioredis.from_url(
            get_redis_url(), encoding="utf8", decode_responses=True
        )
    return redis
