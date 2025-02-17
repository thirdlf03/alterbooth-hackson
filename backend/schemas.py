from pydantic import BaseModel
from typing import Optional
import datetime

class TaskBase(BaseModel):
    name: str
    is_done: bool

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True