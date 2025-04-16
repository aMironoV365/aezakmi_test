import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    read_at = Column(DateTime, nullable=True)

    # Результаты AI-анализа
    category = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    processing_status = Column(String, default="pending")
