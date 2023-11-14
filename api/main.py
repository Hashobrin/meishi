from passlib.context import CryptContext

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()
templates = Jinja2Templates(directory='/src/api/templates')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class User(BaseModel):
    """
    User model
    """
    username: str
    email: Optional[str]
    password: Optional[str]


@app.get('/sayhello')
async def sayhello(req: Request):
    return templates.TemplateResponse(
        'sayhello.html',
        {'request': req, 'name': 'fubii'}
    )


@app.get('/signup')
async def signup_page(req: Request):
    return templates.TemplateResponse('signup.html', {'request': req})


@app.post('/signup')
async def signup(req: Request):
    pwd_context.hash(req)
    response = RedirectResponse(url='/home')
    response.set_cookie(key='access_token', value='generated_token')
    return response


@app.get('/login', response_class=HTMLResponse)
async def login_page(req: Request):
    return templates.TemplateResponse('login.html', {'request': req})


@app.post('/login')
async def login(
    req: Request, form_data: OAuth2PasswordRequestForm = Depends()
):
    response = RedirectResponse(url='/home')
    response.set_cookie(key='access_token', value='generated_token')
    return response


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    if token != 'testusername':
        raise credentials_exception

    return token


@app.get('/home')
async def home_page(
    req: Request, current_user: str = Depends(get_current_user)
):
    return templates.TemplateResponse(
        'home.html', {'request': req, 'current_user': current_user})


@app.get('/items/')
async def read_items(token: str = Depends(oauth2_scheme)):
    return {'token': token}
