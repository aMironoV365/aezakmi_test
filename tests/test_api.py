import pytest
from uuid import uuid4
from app.db.models import Notification
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_notification(client: AsyncClient):
    """
    Этот тест проверяет создание нового уведомления через API. Он отправляет запрос на создание уведомления с данными пользователя, заголовком и текстом.

    Ожидаемое поведение:
    API должен вернуть статус-код 200 OK, подтверждая успешное создание.

    В ответе должны быть возвращены данные уведомления, включая его title и уникальный id.

    Данные:
    user_id: UUID пользователя.

    title: Заголовок уведомления.

    """
    payload = {
        "user_id": str(uuid4()),
        "title": "Test Title",
        "text": "Something went wrong: error in system",
    }

    response = await client.post("/create_notification", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_notification(client: AsyncClient, async_session: AsyncSession):
    """
    Этот тест проверяет получение уведомления по его уникальному id. Он добавляет уведомление в базу данных и отправляет GET-запрос на получение уведомления по ID.

    Ожидаемое поведение:
    API должен вернуть статус-код 200 OK, если уведомление существует.

    Ответ должен содержать правильный title, соответствующий уведомлению в базе данных.

    Данные:
    notif.id: UUID уведомления, которое было добавлено в базу данных.
    """
    notif = Notification(user_id=uuid4(), title="Hello", text="This is a test")
    async_session.add(notif)
    await async_session.commit()
    await async_session.refresh(notif)

    response = await client.get(f"/notification{notif.id}")
    assert response.status_code == 200
    assert response.json()["title"] == notif.title


@pytest.mark.asyncio
async def test_mark_notification_as_read(
    client: AsyncClient, async_session: AsyncSession
):
    """
    Этот тест проверяет, что уведомление можно пометить как прочитанное. Он отправляет POST-запрос на маркер прочтения уведомления и проверяет, что поле read_at обновляется.

    Ожидаемое поведение:
    Статус-код ответа должен быть 200 OK.

    Ответ должен содержать обновленное уведомление с установленным значением в поле read_at (время, когда уведомление было прочитано).

    Данные:
    notif.id: UUID уведомления, которое нужно отметить как прочитанное.
    """
    notif = Notification(user_id=uuid4(), title="Mark this", text="Will be read")
    async_session.add(notif)
    await async_session.commit()
    await async_session.refresh(notif)

    assert notif.read_at is None

    response = await client.post(f"/notification{notif.id}/mark_read")
    assert response.status_code == 200
    assert response.json()["read_at"] is not None


@pytest.mark.asyncio
async def test_list_notifications(client: AsyncClient, async_session: AsyncSession):
    """
    Этот тест проверяет получение списка уведомлений для конкретного пользователя. Он добавляет несколько уведомлений в базу данных и отправляет GET-запрос на получение списка уведомлений по user_id.

    Ожидаемое поведение:
    API должен вернуть статус-код 200 OK и список уведомлений для данного пользователя.

    Количество уведомлений в ответе должно соответствовать количеству добавленных уведомлений (в данном случае 3).

    Данные:
    user_id: UUID пользователя, для которого нужно получить список уведомлений.
    """
    user_id = uuid4()
    for i in range(3):
        notif = Notification(user_id=user_id, title=f"Title {i}", text="Some text")
        async_session.add(notif)
    await async_session.commit()

    response = await client.get("/notification_list", params={"user_id": user_id})
    assert response.status_code == 200
    assert len(response.json()) == 3
