from pydantic import BaseModel
from typing import Optional, List
import datetime

class TaskBase(BaseModel):
    name: str
    priority: str = 'low'  # Added priority
    is_done: Optional[bool] = False  # Optional for updates where it might not be provided


class TaskCreate(TaskBase):
    user_id: int # Added user_id for creation


class TaskUpdate(TaskBase):
    name: Optional[str] = None  # Make fields optional for partial updates
    priority: Optional[str] = None



class Task(TaskBase):
    id: int
    user_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: str
    

class UserCreate(BaseModel):
    email: str
    password: str

class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    point: Optional[int] = None

class UserProfile(BaseModel):
    id: int
    icon: str
    name: str
    profile: str

class UserResponse(BaseModel):
    id: int
    name: Optional[str]
    point: Optional[int]


    class Config:
        orm_mode = True

class UserPoint(BaseModel):
    id: int
    point: int

class User(UserBase):
    id: int
    email: str
    name: str
    point: int
    icon: str
    profile: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class BoardBase(BaseModel):
    content : str
    

class BoardCreate(BoardBase):
    user_id : int

class BoardUpdate(BoardBase):
    content : Optional[str] = None
    
class Board(BoardBase):
    id: int
    user_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True