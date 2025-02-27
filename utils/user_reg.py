from .base_form import BaseValidation
from pydantic import EmailStr, Field
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import timedelta, datetime
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
        examples=['Qwerty1!']
    )
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password: str, hash_password: str) -> bool:
    return pwd_context.verify(secret=password, hash=hash_password)

def create_access_token(sub: str) -> str:
    return jwt.encode(
        claims={
            'sub': sub,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        },
        key=SETTINGS.SECRET_STR.get_secret_value(),
        algorithm="HS256"
    )


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
