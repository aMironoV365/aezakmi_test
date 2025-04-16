import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.models import Base

from app.db.database import get_session


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture()
async def async_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
        await engine.dispose()


@pytest_asyncio.fixture
async def client(async_session):
    """
    Фикстура client предоставляет асинхронного клиента для тестирования FastAPI-приложений.
    Этот клиент позволяет отправлять запросы к приложению в контексте теста,
    заменяя зависимость для получения сессии базы данных на уже существующую сессию,
    предоставляемую фикстурой async_session.
    """

    async def override_get_session():
        yield async_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()
