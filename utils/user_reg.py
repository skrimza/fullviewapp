from .base_form import BaseValidation
from pydantic import EmailStr, Field
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import timedelta, datetime
from typing import Dict
from config import SETTINGS


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
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password: str, hash_password: str) -> bool:
    return pwd_context.verify(secret=password, hash=hash_password)

def create_access_token(data: Dict[str, str]) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SETTINGS.SECRET_STR.get_secret_value(), algorithm="HS256")
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
