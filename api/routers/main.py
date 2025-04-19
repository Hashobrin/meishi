import re

from passlib.context import CryptContext
import typing
from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    HTTPBasic,
    HTTPBasicCredentials,
)
from sqlmodel import select
from starlette.responses import RedirectResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from pydantic import BaseModel, EmailStr
import hashlib
from sqlalchemy.orm import Session

from api.db import get_db
from api.models.user import User

router = APIRouter()
templates = Jinja2Templates(directory='/src/api/templates')
http_basic = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
responses = {
    302: {'description': 'The item was moved'},
    403: {'description': 'Not enough privileges'},
    404: {'description': 'Item not found'},
}


@router.get('/sayhello', responses={**responses, 200: {}})
async def sayhello(req: Request):
    return templates.TemplateResponse(
        'sayhello.html',
        {'request': req, 'name': 'fubii'}
    )


@router.get('/sample_bootstrap')
async def sample_bootstrap(req: Request):
    return templates.TemplateResponse(
        'sample_bootstrap.html', {'request': req})


@router.get('/signup')
async def signup_page(req: Request):
    return templates.TemplateResponse('signup.html', {'request': req})


@router.post('/signup')
async def signup(req: Request, session: Session=Depends(get_db)):
    data = await req.form()
    email = str(data.get('email'))
    password = str(data.get('password'))
    retype = str(data.get('retype'))
    print(f"{email=}, {password=}, {retype=}")

    pattern_email = re.compile(
        r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')
    pattern_pw = re.compile(r'\w{6,20}')
    errors = []
    # is_user_in_db = session.query(User).filter(User.email == email).first()
    stmt = select(User).where(User.email==email)
    result = await session.exec(stmt)
    is_user_in_db = result.first()
    if is_user_in_db:
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

    user = User(email=email, password=password, username='')
    session.add(user)
    session.commit()
    session.close()

    pwd_context.hash(req)
    response = RedirectResponse(url='/home')
    response.set_cookie(key='access_token', value='generated_token')
    return response


@router.get('/login', response_class=HTMLResponse)
async def login_page(req: Request):
    return templates.TemplateResponse('login.html', {'request': req})


@router.post('/login')
async def login(
    req: Request,
    session:Session=Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    credentials: HTTPBasicCredentials = Depends(http_basic),
    email: str = Form(),
    password: str = Form(),
):
    # inputs
    password = hashlib.md5(credentials.password.encode()).hexdigest()

    user = session.query(User).filter(User.email == email).first()
    session.close()

    if user is None or str(user.password) != password:
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


@router.get('/')
async def go_home_as_default(
    req: Request,
    # current_user: str=Depends(get_current_user)
):
    return templates.TemplateResponse('home.html', {'request': req})


@router.get('/home')
async def home_page(
    req: Request, current_user: str = Depends(get_current_user)
):
    return templates.TemplateResponse(
        'home.html', {'request': req, 'current_user': current_user})


@router.get('/items')
async def read_items(token: str = Depends(oauth2_scheme)):
    return {'token': token}
