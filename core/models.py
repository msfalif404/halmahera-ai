from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ApplicationCreate(BaseModel):
    scholarship_id: str
    user_id: str = "HdaynXVC0R3JGKaBlSJCB4zPu1IvwLRV"  # hardcoded for testing
    status: str = "on-progress"


class TaskCreate(BaseModel):
    name: str
    application_id: str
    description: Optional[str] = None
    is_completed: bool = False
    start_date: datetime = Field(default_factory=datetime.now)
    end_date: datetime = Field(default_factory=datetime.now)
