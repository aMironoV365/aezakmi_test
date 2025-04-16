import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    REDIS_URL = os.getenv("REDIS_URL")
    REDIS_BACKEND = os.getenv("REDIS_BACKEND")
    BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_BACKEND


settings = Settings()
