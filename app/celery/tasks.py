from celery import Celery
from app.config.config import settings
from app.ai.mock_ai import analyze_text
from app.db.database import async_session_maker
from app.db.models import Notification
import asyncio


celery = Celery(
    __name__, broker=settings.BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)


@celery.task
def analyze_notification(notification_id: str, text: str):
    """
    Задача Celery для обработки уведомления и анализа текста.

    Принимает ID уведомления и текст для анализа, вызывает асинхронную обработку
    и обновляет статус уведомления в базе данных в зависимости от результата.

    Аргументы:
        notification_id (str): ID уведомления для обновления.
        text (str): Текст для анализа с помощью AI.

    Возвращаемое значение:
        None
    """
    asyncio.run(_process(notification_id, text))


async def _process(notification_id: str, text: str):
    """
    Асинхронный процесс для анализа текста и обновления уведомления в базе данных.

    В этой функции происходит обновление статуса уведомления, выполнение анализа
    текста с использованием AI, а затем обновление дополнительных полей уведомления
    (категория, уверенность и статус обработки).

    Аргументы:
        notification_id (str): ID уведомления для обновления.
        text (str): Текст для анализа с помощью AI.

    Возвращаемое значение:
        None
    """
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
