from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, INTEGER
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import SETTINGS


class Base(DeclarativeBase):
    id = Column(INTEGER, primary_key=True, index=True)
    engine = create_async_engine(
        SETTINGS.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    )
    session = async_sessionmaker(bind=engine)
    
    @declared_attr
    def __tablename__(cls):
        return "".join(
            f"_{i.lower()}" if i.isupper() else i for i in cls.__name__
        ).strip("_")


