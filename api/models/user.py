from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from api.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    first_name = Column(String(256))
    last_name = Column(String(256))
    birth_date = Column(Date)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    skills = relationship("Skill", back_populates="user")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(256), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="skills")

    # def __init__(self, username, email, password):
    #     self.username = username
    #     self.email = email
    #     self.password = password

    # def __str__(self):
    #     return str(self.id) + ':' + self.username
