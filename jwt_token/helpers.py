from datetime import datetime
from fastapi import HTTPException
from database import SessionLocal
from core.security import verify_password
from users.crud import get_user_by_email
from core.settings import settings
from core.security import create_access_token, create_refresh_token
import jwt

async def authenticate_user(email:str, password:str):
    user = get_user_by_email(email=email, db=SessionLocal())
    password_hash = user.password_hash

    if not user:
        return False
    
    if not verify_password(password=password, password_hash=password_hash):
        return False

    return user

def refresh_access_token(refresh_token:str) -> str:
    
    try:
        payload = jwt.decode(jwt=refresh_token, key=settings.REFRESH_JWT_SECRET, algorithms=["HS256"])
        
        if datetime.utcnow() > datetime.fromtimestamp(int(payload.get("exp"))):
            raise HTTPException(
                status_code=400,
                detail="Token Expired"
            )

        user = get_user_by_email(email=payload.get("username"), db=SessionLocal())

        if user:
            return create_access_token(user.email), create_refresh_token(user.email)
    except Exception as e:
        print(e)