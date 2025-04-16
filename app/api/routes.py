import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List
from datetime import datetime, timezone
from app.db.models import Notification
from app.db.database import get_session
from app.pydantic_schemas.schemas import NotificationCreate, NotificationRead
from app.celery.tasks import analyze_notification
from redis.asyncio import Redis
from app.config.redis_conf import get_redis

router = APIRouter()


@router.post(
    "/create_notification",
    response_model=NotificationRead,
    summary="Создание уведомления",
)
async def create_notification(
    data: NotificationCreate, session: AsyncSession = Depends(get_session)
):
    """
    Создание нового уведомления.

    Принимает данные для создания уведомления и сохраняет его в базе данных.
    После сохранения уведомления запускается фоновая задача анализа текста уведомления.

    Аргументы:
        data (NotificationCreate): Данные для создания уведомления.
        session (AsyncSession): Сессия базы данных, передается через Depends.

    Возвращаемое значение:
        NotificationRead: Данные созданного уведомления.
    """
    notification = Notification(user_id=data.user_id, title=data.title, text=data.text)
    session.add(notification)
    await session.commit()
    await session.refresh(notification)
    analyze_notification.delay(notification.id, notification.text)
    return notification


@router.get(
    "/notification_list",
    response_model=List[NotificationRead],
    summary="Получение списка уведомлений",
)
async def list_notifications(
    user_id: UUID,
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
):
    """
    Получение списка уведомлений для указанного пользователя.

    Если данные уже закешированы в Redis, они извлекаются оттуда. В противном случае выполняется запрос к базе данных
    и результат сохраняется в кэш Redis на 60 секунд.

    Аргументы:
        user_id (UUID): ID пользователя, для которого нужно получить уведомления.
        skip (int): Количество пропускаемых уведомлений для пагинации (по умолчанию 0).
        limit (int): Максимальное количество уведомлений в ответе (по умолчанию 10).
        session (AsyncSession): Сессия базы данных, передается через Depends.
        redis (Redis): Экземпляр Redis, передается через Depends.

    Возвращаемое значение:
        List[NotificationRead]: Список уведомлений пользователя.
    """
    key = f"notifications:{user_id}:{skip}:{limit}"
    cached = await redis.get(key)
    if cached:
        return [NotificationRead(**item) for item in json.loads(cached)]

    stmt = (
        select(Notification)
        .where(Notification.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(stmt)
    notifications = result.scalars().all()

    await redis.set(
        key,
        json.dumps(
            jsonable_encoder([NotificationRead.from_orm(n) for n in notifications])
        ),
        ex=60,
    )
    return notifications


@router.get(
    "/notification{notification_id}",
    response_model=NotificationRead,
    summary="Получение уведомления по ID",
)
async def get_notification(
    notification_id: UUID, session: AsyncSession = Depends(get_session)
):
    """
    Получение уведомления по его ID.

    Аргументы:
        notification_id (UUID): ID уведомления для получения.
        session (AsyncSession): Сессия базы данных, передается через Depends.

    Возвращаемое значение:
        NotificationRead: Уведомление с указанным ID.
    """
    notification = await session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.post(
    "/notification{id}/mark_read",
    response_model=NotificationRead,
    summary="Отметить уведомление как прочитанное",
)
async def mark_as_read(id: UUID, session: AsyncSession = Depends(get_session)):
    """
    Отметить уведомление как прочитанное.

    Обновляет поле `read_at` уведомления и сохраняет изменения в базе данных.

    Аргументы:
        id (UUID): ID уведомления для пометки как прочитанное.
        session (AsyncSession): Сессия базы данных, передается через Depends.

    Возвращаемое значение:
        NotificationRead: Обновленное уведомление.
    """
    notification = await session.get(Notification, id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.read_at = datetime.now(timezone.utc)
    await session.commit()
    await session.refresh(notification)
    return notification
