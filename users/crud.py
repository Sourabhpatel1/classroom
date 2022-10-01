from datetime import datetime
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate
from deps import oauth2_scheme
from core.security import get_password_hash
from .utils import decode_token
from deps import get_db

def register_user(user:UserCreate, db:Session):
    password_hash=get_password_hash(user.password)
    user_obj = User(name=user.name, email=user.email, password_hash=password_hash)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

def get_user_by_email(email:str, db:Session):
    
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    return user

def get_authenticated_user(db:Session = Depends(get_db), token:str = Depends(oauth2_scheme)):
        try:
            payload = decode_token(token)
            td = payload.get('exp')
            if datetime.utcnow() > datetime.fromtimestamp(int(td)):
                raise HTTPException(
                    status_code=401,
                    detail="Token Expired"
                )

            username = payload.get("username")
            user = db.query(User).filter(User.email == username).first()
        except:
            raise HTTPException(status_code=404, detail="User Not Found Or User Not Authenticated, Please Login/Register") 
        
        if not user:
            raise HTTPException(status_code=404, detail="User Not Found Or User Not Authenticated, Please Login / Register")

        return user