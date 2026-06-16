from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel):
    camera_id: str
    timestamp: datetime
    event_type: str
    confidence: float
