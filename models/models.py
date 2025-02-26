from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Users(Base):
    id = ...
    name = ...