from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class NotificationCreate(BaseModel):
    user_id: UUID
    title: str
    text: str


class NotificationRead(BaseModel):
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
        from_attributes = True
    
