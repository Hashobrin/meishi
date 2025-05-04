import configparser

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlmodel.ext.asyncio.session import AsyncSession

config = configparser.ConfigParser()
config_ini_path = 'api/config.ini'

config.read(config_ini_path, encoding='utf-8')
User, Pass, Host, Port = (
    config.get('DEVELOP', 'User'),
    config.get('DEVELOP', 'Pass'),
    config.get('DEVELOP', 'Host'),
    config.get('DEVELOP', 'Port'),
)

db_url = 'mysql+aiomysql://root@db:3306/db_for_app?charset=utf8mb4'
engine = create_async_engine(db_url, echo=True)

Base = declarative_base()

async def get_db():
    async with AsyncSession(engine) as session:
        yield session
