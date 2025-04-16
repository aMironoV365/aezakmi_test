import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    """
    Класс настроек для приложения.

    Загружает настройки, такие как URL для подключения к Redis,
    а также информацию о брокере и бэкенде для Celery.

    Атрибуты:
        REDIS_URL (str): URL для подключения к Redis.
        REDIS_BACKEND (str): URL для бэкенда Redis.
        BROKER_URL (str): URL брокера сообщений (по умолчанию REDIS_URL).
        CELERY_RESULT_BACKEND (str): URL для бэкенда результатов Celery (по умолчанию REDIS_BACKEND).
    """

    REDIS_URL = os.getenv("REDIS_URL")
    REDIS_BACKEND = os.getenv("REDIS_BACKEND")
    BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_BACKEND


settings = Settings()
