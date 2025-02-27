from fastapi import APIRouter, status, Request, HTTPException
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.user_reg import RegForm, pwd_context, verify_password, create_access_token
from utils.token import TokenData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.base_models import Users



router = APIRouter(
    default_response_class=HTMLResponse
)

templates = Jinja2Templates(directory="templates")

@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model_exclude={'password'},
    name="register"
)
async def register_user(form: RegForm, session: AsyncSession):
    result = await Users.session.execute(select(Users).where(Users.email == form.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(form.password)
    new_user = Users(email=form.email, hashed_password=hashed_password)
    Users.session.add(new_user)
    await Users.session.commit()
    await Users.session.refresh(new_user)

@router.post(
    path='/login',
    status_code=status.HTTP_200_OK,
    response_model=TokenData,
    name='Авторизация'
)
async def login(form: RegForm, session: AsyncSession):
    user = session.scalar(select(Users).filter_by(email=form.email))

    if not verify_password(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='incorrect password')

    token = create_access_token(sub=user.id)
    return TokenData(
        access_token=token
    )