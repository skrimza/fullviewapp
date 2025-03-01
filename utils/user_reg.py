from .base_form import BaseValidation
from pydantic import EmailStr, Field
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import timedelta, datetime
from typing import Dict
from config import SETTINGS
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.base import Base, get_session
from models.base_models import Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegForm(BaseValidation):
    email: EmailStr = Field(
        default=...,
        title='User email',
        description='User unique email',
        examples=['jone@doe.com', 'info@mail.com']
    )
    password: str = Field(
        default=...,
        title='User password',
        examples=['Qwerty1!'],
        min_length=7
    )

def verify_password(password: str, hash_password: str) -> bool:
    return pwd_context.verify(secret=password, hash=hash_password)

def create_access_token(data: Dict[str, str]) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        SETTINGS.SECRET_STR.get_secret_value(), 
        algorithm="HS256"
    )
    return encoded_jwt


def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token=token,
            key=SETTINGS.SECRET_STR.get_secret_value(),
            algorithms="HS256"
        )
    except JWTError:
        return {}
    else:
        return payload

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    session: AsyncSession = Depends(get_session)
):
    try:
        payload = jwt.decode(token, SETTINGS.SECRET_STR.get_secret_value(), algorithms=["HS256"])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        result = await session.execute(select(Users).where(Users.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")