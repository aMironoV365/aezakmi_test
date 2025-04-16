from fastapi import FastAPI
from app.db.database import engine
from app.db.models import Base
from contextlib import asynccontextmanager
from app.api.routes import router as ai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекст жизненного цикла приложения:
    - создание таблиц при запуске
    - закрытие соединения при остановке
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(ai_router, tags=["Notifications"])
