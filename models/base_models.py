from sqlalchemy import Column, VARCHAR, BOOLEAN, DECIMAL, DateTime, TEXT, ForeignKey, INTEGER
from .base import Base


class Users(Base):
    email = Column(VARCHAR(254), nullable=False, unique=True)
    hashed_password = Column(nullable=False)
    is_active = Column(BOOLEAN, default=False)
    

class WeatherData(Base):
    city = Column(VARCHAR(100), nullable=False)
    timestamp = Column(DateTime, default=DateTime.utcnow)
    temperature = Column(DECIMAL, nullable=False)
    description = Column(TEXT, nullable=False)
    user_id = Column(INTEGER, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)