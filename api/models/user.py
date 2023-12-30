import os
import sys

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

sys.path.append(os.pardir)
from api.db import Base


class User(Base):
    """
    User model
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(256))
    email = Column(String(256))
    password = Column(String(256))

    # def __init__(self, username, email, password):
    #     self.username = username
    #     self.email = email
    #     self.password = password

    # def __str__(self):
    #     return str(self.id) + ':' + self.username
