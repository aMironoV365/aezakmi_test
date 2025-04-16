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

@router.post("/", response_model=NotificationRead)
async def create_notification(data: NotificationCreate, session: AsyncSession = Depends(get_session)):
    notification = Notification(
        user_id=data.user_id,
        title=data.title,
        text=data.text
    )
    session.add(notification)
    await session.commit()
    await session.refresh(notification)
    analyze_notification.delay(notification.id, notification.text)
    return notification

@router.get("/", response_model=List[NotificationRead])
async def list_notifications(
    user_id: UUID,
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
):
    key = f"notifications:{user_id}:{skip}:{limit}"
    cached = await redis.get(key)
    if cached:
        return [NotificationRead(**item) for item in json.loads(cached)]

    stmt = select(Notification).where(Notification.user_id == user_id).offset(skip).limit(limit)
    result = await session.execute(stmt)
    notifications = result.scalars().all()
    
    await redis.set(
    key,
    json.dumps(jsonable_encoder([NotificationRead.from_orm(n) for n in notifications])),
    ex=60
)
    return notifications

@router.get("/{notification_id}", response_model=NotificationRead)
async def get_notification(notification_id: UUID, session: AsyncSession = Depends(get_session)):
    notification = await session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.post("/{id}/mark_read", response_model=NotificationRead)
async def mark_as_read(id: UUID, session: AsyncSession = Depends(get_session)):
    notification = await session.get(Notification, id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.read_at = datetime.now(timezone.utc)
    await session.commit()
    await session.refresh(notification)
    return notification