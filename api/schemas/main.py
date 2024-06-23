from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    nickname: Optional[str]=Field(None)

class UserCreate(UserBase):
    pass

class UserCreateResponse(UserCreate):
    id: int

    class Config:
        orm_mode=True
