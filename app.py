from fastapi import FastAPI
from handlers.web.web import router as web_router
from handlers.login.login import router as login_router
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount(
    path='/static',
    app=StaticFiles(directory='static'),
    name='static'
)

app.include_router(router=web_router)
app.include_router(router=login_router)
