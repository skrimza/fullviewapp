from fastapi import status, Request
from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    default_response_class=HTMLResponse
)

templates = Jinja2Templates(directory="templates")


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    name="index"
)
async def web_app(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={
            "request": request
        }
        
    )