import re
from passlib.context import CryptContext

from fastapi import FastAPI, Request, Depends, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    HTTPBasic,
    HTTPBasicCredentials,
)
from starlette.responses import RedirectResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from pydantic import BaseModel, EmailStr
import hashlib

from sample_table import SampleUser, session

app = FastAPI()
templates = Jinja2Templates(directory='/src/api/templates')
http_basic = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class User(BaseModel):
    """
    User model
    """
    username: str
    email: EmailStr
    password: str


@app.get('/sayhello')
async def sayhello(req: Request) -> Jinja2Templates:
    return templates.TemplateResponse(
        'sayhello.html',
        {'request': req, 'name': 'fubii'}
    )


@app.exception_handler(404)
async def not_found(req: Request, exc: HTTPException) -> Jinja2Templates:
    return templates.TemplateResponse('404.html', {'request': req})


@app.get('/signup')
async def signup_page(req: Request) -> Jinja2Templates:
    return templates.TemplateResponse('signup.html', {'request': req})


@app.post('/signup')
async def signup(req: Request) -> RedirectResponse:
    data = await req.form()
    email = data.get('email')
    password = data.get('password')
    retype = data.get('retype')

    pattern_email = re.compile(
        r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')
    pattern_pw = re.compile(r'\w{6,20}')
    errors = []
    user_in_db = session.query(SampleUser)\
        .filter(SampleUser.email == email).first()
    if user_in_db is not None:
        errors.append('user e-mail already exist.')
    if password != retype:
        errors.append('doesn\'t matched passwords.')
    if pattern_email.match(email) is None:
        errors.append('wrong e-mail address.')
    if pattern_pw.match(password) is None:
        errors.append('Please use half-width alphanumeric characters for your password between 6 and 20 characters.')

    if errors:
        return templates.TemplateResponse(
            'signup.html', {'request': req, 'email': email, 'errors': errors})

    user = SampleUser(email=email, password=password)
    session.add(user)
    session.commit()
    session.close()

    pwd_context.hash(req)
    response = RedirectResponse(url='/home')
    response.set_cookie(key='access_token', value='generated_token')
    return response


@app.get('/login', response_class=HTMLResponse)
async def login_page(req: Request) -> Jinja2Templates:
    return templates.TemplateResponse('login.html', {'request': req})


@app.post('/login')
async def login(
    req: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    credentials: HTTPBasicCredentials = Depends(http_basic),
    email: str = Form(),
    password: str = Form(),
) -> Jinja2Templates:
    # inputs
    email = credentials.email
    password = hashlib.md5(credentials.password.encode()).hexdigest()

    user = session.query(SampleUser)\
        .filter(SampleUser.email == email).first()
    session.close()

    if user is None or user.password != password:
        error = 'wrong email or password...'
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={'WWW-Authenticate': 'Basic'},
        )
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
