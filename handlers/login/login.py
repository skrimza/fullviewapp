from fastapi import APIRouter, status, HTTPException, Depends
from utils.user_reg import RegForm, pwd_context, verify_password, create_access_token
from starlette.responses import JSONResponse
from utils.token import TokenData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.base_models import Users
from typing import Annotated

router = APIRouter()

async def get_session() -> AsyncSession:
    from models.base import Base
    async with Base.session() as session:
        yield session

@router.post(
    path="/register", 
    status_code=status.HTTP_201_CREATED, 
    response_model=RegForm
)
async def register_user(form: RegForm, session: Annotated[AsyncSession, Depends(get_session)]):
    result = await session.execute(select(Users).where(Users.email == form.email))
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if not form.password:
        raise HTTPException(status_code=400, detail="Password cannot be empty")
    hashed_password = pwd_context.hash(form.password)
    new_user = Users(email=form.email, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return JSONResponse({"email": new_user.email, "message": "User registered successfully"})


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    name="login",
    response_model=TokenData
)
async def login(form: RegForm, session: Annotated[AsyncSession, Depends(get_session)]):
    try:
        result = await session.execute(select(Users).filter_by(email=form.email))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

        if not verify_password(form.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")
        token = create_access_token(data={"sub": str(user.id)})
        return TokenData(access_token=token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))