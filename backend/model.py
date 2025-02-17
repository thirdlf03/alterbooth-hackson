import datetime

from sqlalchemy import (Column, DateTime, Integer, Boolean, String, Enum, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, default="Guest")
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    point = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    tasks = relationship("Task", back_populates="user")  # Relationship to Task
    boards = relationship("Board", back_populates="user") # Relationship to Board


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign Key
    name = Column(String(255), nullable=False)
    priority = Column(Enum('low', 'medium', 'high'), nullable=False, default='low')
    is_done = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="tasks")  # Relationship to User


class Board(Base):
    __tablename__ = 'boards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False) # Foreign Key
    content = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="boards") 