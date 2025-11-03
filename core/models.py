from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    scholarship_id: str
    user_id: str = "HdaynXVC0R3JGKaBlSJCB4zPu1IvwLRV"  # hardcoded for testing
    status: str = "on-progress"


class TaskCreate(BaseModel):
    name: str
    application_id: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str = "pending"
