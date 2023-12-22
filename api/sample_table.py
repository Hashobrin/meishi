import os

import hashlib
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import INTEGER

base = declarative_base()
rdb_path = 'sqlite:///db.sqlite3'
engine = create_engine(rdb_path, echo=True)
session_maker = sessionmaker(bind=engine)
session = session_maker()


class SampleUser(base):
    __tablename__ = 'users'
    id = Column(
        'id', INTEGER(unsigned=True), primary_key=True, autoincrement=True
    )
    username = Column('username', String(256))
    password = Column('password', String(256))
    email = Column('email', String(256))

    def __init__(self, username, password, email):
        self.username = username
        self.password = hashlib.md5(password.encode()).hexdigest()
        self.email = email

    def __str__(self):
        return str(self.id) + ':' + self.username


def main():
    if not os.path.isfile(rdb_path):
        base.metadata.create_all(bind=engine)

    admin = SampleUser(
        username='admin', password='fastapi', email='hoge@example.com')
    session.add(admin)
    session.commit()
    session.close()


if __name__ == '__main__':
    main()
