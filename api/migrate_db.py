<<<<<<< HEAD
from sqlalchemy import create_engine

from api.models.user import Base

db_url = 'mysql+pymysql://root@db:3306/dev?charset=utf8'
engine = create_engine(db_url, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    reset_database()
=======
from sqlalchemy import create_engine

from api.models.task import Base

db_url = 'mysql+pymysql://root@db:3306/dev?charset=utf8'
engine = create_engine(db_url, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    reset_database()
>>>>>>> dec1c67e01e70e1720e3a779c7ff2c21e0521480
