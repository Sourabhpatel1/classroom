from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from users.models import User
from .schemas import UserResponse, UserCreate
from .crud import register_user, get_authenticated_user
from deps import get_db

user_router = APIRouter()

@user_router.post("/add_user", response_model=UserResponse)
def add_user(user:UserCreate, db:Session=Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email Already Registered Please Login"
        )
    user = register_user(user=user,db=db)
    return user

@user_router.get('/users/me', response_model=UserResponse)
def get_current_user(user:UserResponse = Depends(get_authenticated_user)):
    return user

@user_router.get("/logout")
def logout_user(response:Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"Message" : "Logged Out Succesfully"}