from fastapi import FastAPI, Request, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.include_router(router)
router = APIRouter()
templates = Jinja2Templates(directory='meishi/templates')

@router.get('/sayhello')
async def sayhello(name: str, request: Request):
    return templates.TemplateResponse(
        'sayhello.html',
        {'name': name, 'request': request}
    )
