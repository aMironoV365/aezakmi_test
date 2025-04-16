from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class NotificationCreate(BaseModel):
    """
    Модель для создания уведомления.

    Эта модель используется для валидации данных, передаваемых при создании нового уведомления.

    Атрибуты:
    - user_id (UUID): Уникальный идентификатор пользователя, для которого создается уведомление.
    - title (str): Заголовок уведомления.
    - text (str): Текст уведомления.
    """

    user_id: UUID
    title: str
    text: str


class NotificationRead(BaseModel):
    """
    Модель для чтения уведомления.

    Эта модель используется для представления уведомлений, которые были получены из базы данных или другого источника.

    Атрибуты:
    - id (UUID): Уникальный идентификатор уведомления.
    - user_id (UUID): Уникальный идентификатор пользователя, которому принадлежит уведомление.
    - title (str): Заголовок уведомления.
    - text (str): Текст уведомления.
    - created_at (datetime): Дата и время создания уведомления.
    - read_at (Optional[datetime]): Дата и время, когда уведомление было прочитано. Может быть пустым, если уведомление не было прочитано.
    - category (Optional[str]): Категория уведомления. Может быть пустым.
    - confidence (Optional[float]): Уровень уверенности в содержимом уведомления. Может быть пустым.
    - processing_status (str): Статус обработки уведомления (например, 'pending', 'processed').
    """

    id: UUID
    user_id: UUID
    title: str
    text: str
    created_at: datetime
    read_at: Optional[datetime]
    category: Optional[str]
    confidence: Optional[float]
    processing_status: str

    class Config:
        """
        Конфигурация модели для Pydantic.

        Включает настройку для автоматического извлечения данных из атрибутов модели, что позволяет работать с объектами, полученными через ORM.
        """

        from_attributes = True
