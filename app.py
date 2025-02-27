from fastapi import FastAPI
from handlers.web.web import router
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount(
    path='/static',
    app=StaticFiles(directory='static'),
    name='static'
)

app.include_router(router=router)
