import configparser
from sqlalchemy.ext.asyncio import create_async_engine

from api.models.user import Base

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
User, Pass, Host, Port = (
    config.get('DEVELOP', 'User'),
    config.get('DEVELOP', 'Pass'),
    config.get('DEVELOP', 'Host'),
    config.get('DEVELOP', 'Port'),
)
db_url = f'{User}://{Pass}@{Host}:{Port}/dev?charset=utf8'
engine = create_async_engine(db_url, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    reset_database()
