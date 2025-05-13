import re

from passlib.context import CryptContext
from typing import Optional, Dict, Any

from fastapi import Request, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowPassword
from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    HTTPBasic,
    HTTPBasicCredentials,
    OAuth2,
)
from sqlalchemy import select
from starlette.responses import RedirectResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from pydantic import BaseModel, EmailStr
import hashlib
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db
from api.models.user import User


class OAuth2PasswordBearerWithCookie(OAuth2):
    """
    OAuth2 password flow with support for both header and cookie authentication
    """
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password=OAuthFlowPassword(tokenUrl=tokenUrl, scopes=scopes))
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        # First try to get the token from the header
        authorization: Optional[str] = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        
        if not authorization or scheme.lower() != "bearer":
            # If not in header, try to get from cookie
            token = request.cookies.get("access_token")
            if not token and self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return token
        return param

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
async def signup(req: Request, session: AsyncSession = Depends(get_db)):
    try:
        data = await req.form()
        email = str(data.get('email'))
        password = str(data.get('password'))
        retype = str(data.get('retype'))
        print(f"{email=}, {password=}, {retype=}")

        pattern_email = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')
        pattern_pw = re.compile(r'\w{6,20}')
        errors = []
        
        # 既存ユーザーの確認
        stmt = select(User).where(User.email==email)
        print(stmt.compile(compile_kwargs={"literal_binds": True}))
        result = await session.execute(stmt)
        users = result.scalars().all()
        print(f'{users=}')
        existing_user = result.scalar_one_or_none()
        if existing_user:
            errors.append('このメールアドレスは既に登録されています。')
        
        # パスワードの一致確認
        if password != retype:
            errors.append('パスワードが一致しません。')
        
        # メールアドレスの形式確認
        if pattern_email.match(email) is None:
            errors.append('メールアドレスの形式が正しくありません。')
        
        # パスワードの形式確認
        if pattern_pw.match(password) is None:
            errors.append('パスワードは6文字以上20文字以下の半角英数字で入力してください。')

        if errors:
            print(f"{errors=}")
            return templates.TemplateResponse(
                'signup.html', {'request': req, 'email': email, 'messages': errors})

        hashed_password = pwd_context.hash(password)
        user = User(email=email, password=hashed_password, username=email.split('@')[0])
        session.add(user)
        await session.commit()

        response = RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)
        response.set_cookie(key='access_token', value='generated_token')
        return response

    except Exception as e:
        await session.rollback()
        errors = ['登録中にエラーが発生しました。もう一度お試しください。']
        print(f"エラーの詳細: {str(e)}")
        print(f"エラーの型: {type(e)}")
        print(f"{errors=}")
        return templates.TemplateResponse(
            'signup.html', {'request': req, 'email': email, 'messages': errors})


@router.get('/login', response_class=HTMLResponse)
async def login_page(req: Request):
    return templates.TemplateResponse('login.html', {'request': req})


@router.post('/login')
async def login(
    req: Request,
    session: AsyncSession = Depends(get_db),
    email: str = Form(),
    password: str = Form(),
):
    result = await session.execute(select(User).where(User.email==email))
    user = result.scalar_one_or_none()
    
    if user is None or not pwd_context.verify(password, str(user.password)):
        error = 'メールアドレスまたはパスワードが正しくありません。'
        return templates.TemplateResponse(
            'login.html', 
            {'request': req, 'email': email, 'messages': [error]}
        )
    
    response = RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)
    response.set_cookie(key='access_token', value='generated_token')
    return response


async def get_current_user(req: Request):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    token = req.cookies.get('access_token')
    if not token:
        return RedirectResponse(url='/login', status_code=status.HTTP_302_FOUND)

    if token != 'generated_token':
        return RedirectResponse(url='/login', status_code=status.HTTP_302_FOUND)

    return token


@router.get('/')
async def go_home_as_default(
    req: Request,
    current_user: str=Depends(get_current_user)
):
    return templates.TemplateResponse('home.html', {'request': req, 'current_user': current_user})


@router.get('/logout')
async def logout(req: Request):
    response = RedirectResponse(url='/login', status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key='access_token')
    return response


@router.get('/home')
async def home_page(
    req: Request,
    current_user: str = Depends(get_current_user)
):
    return templates.TemplateResponse(
        'home.html', {'request': req, 'current_user': current_user})


@router.get('/items')
async def read_items(token: str = Depends(oauth2_scheme)):
    return {'token': token}
