import datetime

from sqlalchemy import (Column, DateTime, Integer, Boolean, String)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    is_done = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

class Board(Base):
    __tablename__ = 'boards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)


