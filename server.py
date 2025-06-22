from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from src.routers.PesananRoute import router as pr
from src.routers.UserRoute import router as ur
from src.routers.MenuRoute import router as mr
from src.routers.AuthRoute import router as ar

app = FastAPI()
app.mount('/media', StaticFiles(directory='media'), name='media')

app.include_router(ar)
app.include_router(pr)
app.include_router(ur)
app.include_router(mr)