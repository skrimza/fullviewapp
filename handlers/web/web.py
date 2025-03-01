from fastapi import APIRouter, Request, status, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.base import get_session
from models.base_models import WeatherData, Users
from handlers.api_weather.api_client import ApiClient
from googletrans import Translator
from utils.user_reg import get_current_user
from typing import Annotated
import logging

router = APIRouter(default_response_class=HTMLResponse)
templates = Jinja2Templates(directory="templates")
translator = Translator()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    name="index"
)
async def web_app(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request}
    )

@router.get(
    path="/weather",
    status_code=status.HTTP_200_OK,
    name="weather",
    response_class=HTMLResponse
)
async def get_weather(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Users = Depends(get_current_user)
):
    client_data = dict(request.query_params)

    city = client_data.get("city")
    day = client_data.get("day")
    if not city or not day:
        raise HTTPException(status_code=400, detail="City and day are required")
    try:
        translated = translator.translate(text=city, src="ru", dest="en")
        weather_request = ApiClient()
        weather_response = weather_request.get_weather_data(q=translated.text, days=day)
        weather_entry = WeatherData(
            city=weather_response["location"]["name"],
            temperature=weather_response["forecast"]["forecastday"][0]["day"]["maxtemp_c"],
            description=weather_response["forecast"]["forecastday"][0]["day"]["condition"]["text"],
            user_id=current_user.id
        )
        session.add(weather_entry)
        await session.commit()
        await session.refresh(weather_entry)
        weather_data = {
            "city": weather_response["location"]["name"],
            "time": weather_response["location"]["localtime"],
            "data": weather_response["forecast"]["forecastday"]
        }
        
        return templates.TemplateResponse(
            name="wather-table.html",
            context={"request": request, **weather_data}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.get(
    path="/weather_data",
    status_code=status.HTTP_200_OK,
    name="weather_data",
    response_class=HTMLResponse
)
async def get_weather_data(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Users = Depends(get_current_user)
):
    try:
        result = await session.execute(
            select(WeatherData).where(WeatherData.user_id == current_user.id)
        )
        weather_entries = result.scalars().all()
        context = {
            "request": request,
            "weather_entries": weather_entries
        }
        
        return templates.TemplateResponse(
            name="data-weather.html",
            context=context
        )
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
