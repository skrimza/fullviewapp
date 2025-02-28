from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import SETTINGS




class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, index=True)
    engine = create_async_engine(
    SETTINGS.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
        echo=True
    )
    session = async_sessionmaker(bind=engine)

    @declared_attr
    def __tablename__(cls) -> str:
        return "".join(
            f"_{i.lower()}" if i.isupper() else i for i in cls.__name__
        ).strip("_")