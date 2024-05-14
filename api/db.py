from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker)
from sqlalchemy.orm import declarative_base, DeclarativeBase

async_db_url = "mysql+aiomysql://root@db:3306/dev?charset=utf8"

async_engine = create_async_engine(async_db_url, echo=True)
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
