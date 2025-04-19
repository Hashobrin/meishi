from datetime import datetime
import os
import sys
from typing import Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlmodel import Field, SQLModel

# sys.path.append(os.pardir)
from api.db import Base


class User(SQLModel, table=True):
    """
    User model
    """

    # __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # def __init__(self, username, email, password):
    #     self.username = username
    #     self.email = email
    #     self.password = password

    # def __str__(self):
    #     return str(self.id) + ':' + self.username
