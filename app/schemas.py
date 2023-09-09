from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    publish: bool = True

class UserPost(BaseModel):
    id: int
    email : EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class PostCreate(PostBase):
    pass 

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserPost 

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email : EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    class Config:
        orm_mode = True

class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)