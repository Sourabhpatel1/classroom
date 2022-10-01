from pydantic import BaseModel, EmailStr
from datetime import datetime


# Response Model

class UserResponse(BaseModel):
    name:str
    email:EmailStr

    class Config:
        orm_mode=True


# User Create Model

class UserCreate(UserResponse):
    password:str
    

class UserSchema(UserCreate):
    id:int
    is_admin:bool
    is_creator:bool