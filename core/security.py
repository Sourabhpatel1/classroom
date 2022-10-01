from datetime import datetime, timedelta
import bcrypt
from typing import Union, Any
from core.settings import settings
import jwt

def get_password_hash(password:str)->str:
    
    # convert to byte
    byt = password.encode('utf-8')
    
    # generate salt
    salt = bcrypt.gensalt()
    
    # hash password -> returns bytes
    password_hash_byt = bcrypt.hashpw(byt, salt)
    
    # return string hash
    return password_hash_byt.decode('utf-8')


def verify_password(password:str, password_hash:str) -> bool:

    #encode str to bytes
    password = password.encode('utf-8')
    password_hash = password_hash.encode('utf-8')

    # Check and return -> Returns Boolean
    return bcrypt.checkpw(password, password_hash)


def create_access_token(subject:str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_DELTA)
    
    payload = {"exp" : expires_delta, "username" : subject}
    
    access_token = jwt.encode(payload=payload, key=settings.ACCESS_JWT_SECRET, algorithm="HS256").decode('utf-8')

    return access_token


def create_refresh_token(subject:str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_DELTA)
    
    payload = {"exp" : expires_delta, "username" : subject}
    
    refresh_token = jwt.encode(payload=payload, key=settings.REFRESH_JWT_SECRET, algorithm="HS256").decode('utf-8')

    return refresh_token