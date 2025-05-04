# import os, errno
import time

import configparser
import asyncio
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine

from api.models.user import Base

config = configparser.ConfigParser()
config_ini_path = 'api/config.ini'

# if not os.path.exists(config_ini_path):
#     raise FileNotFoundError(
#         errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)

# config.read(config_ini_path, encoding='utf-8')
# User, Pass, Host, Port = (
#     config.get('DEVELOP', 'User'),
#     config.get('DEVELOP', 'Pass'),
#     config.get('DEVELOP', 'Host'),
#     config.get('DEVELOP', 'Port'),
# )
# db_url = f'{User}://{Pass}@{Host}:{Port}/dev?charset=utf8'
db_url = 'mysql+aiomysql://root@db:3306/db_for_app?charset=utf8mb4'
engine = create_async_engine(db_url, echo=True)

# 接続リトライ
async def wait_for_db(max_retries=10, delay=2):
    for i in range(max_retries):
        try:
            async with engine.begin() as conn:
                await conn.execute(text('SELECT 1'))
            print("✅ DB connection established.")
            return
        except OperationalError:
            print(f"⏳ Waiting for DB... ({i+1}/{max_retries})")
            time.sleep(delay)
    raise RuntimeError("❌ Could not connect to the database.")

async def reset_database():
    await wait_for_db()
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(reset_database())
