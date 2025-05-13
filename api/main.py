from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, HTTPBasic
from starlette.responses import RedirectResponse

from .routers import main as main_router
from .routers.main import templates

app = FastAPI()


@app.exception_handler(404)
def not_found(req: Request, exc: HTTPException):
    return templates.TemplateResponse('404.html', {'request': req})

@app.exception_handler(401)
def unauthorized(req: Request, exc: HTTPException):
    return RedirectResponse(url='/login')


router = APIRouter()
router.include_router(main_router.router, tags=['main'])

app.include_router(router)

app.mount('/static', StaticFiles(directory='api/static'), name='static')
