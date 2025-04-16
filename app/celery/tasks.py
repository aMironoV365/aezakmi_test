from celery import Celery
from app.config.config import settings
from app.ai.mock_ai import analyze_text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import async_session_maker
from app.db.models import Notification
import asyncio

celery = Celery(__name__, broker=settings.BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

@celery.task
def analyze_notification(notification_id: str, text: str):
    asyncio.run(_process(notification_id, text))

async def _process(notification_id: str, text: str):
    async with async_session_maker() as session:
        notification = await session.get(Notification, notification_id)
        if not notification:
            return
        notification.processing_status = "processing"
        await session.commit()

        try:
            result = await analyze_text(text)
            notification.category = result["category"]
            notification.confidence = result["confidence"]
            notification.processing_status = "completed"
        except:
            notification.processing_status = "failed"
        await session.commit()