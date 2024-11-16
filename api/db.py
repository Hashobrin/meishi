import configparser

from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker)
from sqlalchemy.orm import declarative_base, DeclarativeBase

# async_db_url = "mysql+aiomysql://root@db:3306/dev?charset=utf8"
config = configparser.ConfigParser()
config_ini_path = 'api/config.ini'

config.read(config_ini_path, encoding='utf-8')
User, Pass, Host, Port = (
    config.get('DEVELOP', 'User'),
    config.get('DEVELOP', 'Pass'),
    config.get('DEVELOP', 'Host'),
    config.get('DEVELOP', 'Port'),
)
db_url = f'{User}://{Pass}@{Host}:{Port}/dev?charset=utf8'

async_engine = create_async_engine(db_url, echo=True)
async_session = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()
# class Base(DeclarativeBase):
#     """
#     docstring
#     """
#     pass


async def get_db():
    async with async_session() as session:
        yield session
