from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApplicationCreate(BaseModel):
    scholarship_id: str
    user_id: str
    status: str = "on-progress"

class TaskCreate(BaseModel):
    name: str
    application_id: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str = "pending"