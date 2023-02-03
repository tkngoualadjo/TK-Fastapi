from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
import os
from pydantic import BaseSettings
from dotenv import load_dotenv

# modele 


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True



#spécifie le schéma de reponse 
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


#class jointure 
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True   

class UserCreate(BaseModel):
    email: EmailStr
    password: str



#login user

class UserLogin(BaseModel):
    email: EmailStr
    password: str

#le schema du token

class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)