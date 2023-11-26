from passlib.context import CryptContext
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, HTTPBasic

from .routers import main

app = FastAPI()
templates = Jinja2Templates(directory='/src/api/templates')
http_basic = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

app.include_router(main.router)
