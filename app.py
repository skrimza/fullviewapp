from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from handlers import router

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount(
    path='/static',
    app=StaticFiles(directory='static'),
    name='static'
)

app.include_router(router=router)