import pytest
import asyncio
from uuid import uuid4
from app.db.models import Notification
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_notification(client: AsyncClient):
    payload = {
        "user_id": str(uuid4()),
        "title": "Test Title",
        "text": "Something went wrong: error in system",
    }

    response = await client.post("/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_notification(client: AsyncClient, async_session: AsyncSession):
    notif = Notification(user_id=uuid4(), title="Hello", text="This is a test")
    async_session.add(notif)
    await async_session.commit()
    await async_session.refresh(notif)

    response = await client.get(f"/{notif.id}")
    assert response.status_code == 200
    assert response.json()["title"] == notif.title


@pytest.mark.asyncio
async def test_mark_notification_as_read(
    client: AsyncClient, async_session: AsyncSession
):
    notif = Notification(user_id=uuid4(), title="Mark this", text="Will be read")
    async_session.add(notif)
    await async_session.commit()
    await async_session.refresh(notif)

    assert notif.read_at is None

    response = await client.post(f"/{notif.id}/mark_read")
    assert response.status_code == 200
    assert response.json()["read_at"] is not None


@pytest.mark.asyncio
async def test_list_notifications(client: AsyncClient, async_session: AsyncSession):
    user_id = uuid4()
    for i in range(3):
        notif = Notification(user_id=user_id, title=f"Title {i}", text="Some text")
        async_session.add(notif)
    await async_session.commit()

    response = await client.get("/", params={"user_id": user_id})
    assert response.status_code == 200
    assert len(response.json()) == 3
