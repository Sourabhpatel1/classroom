import jwt
from jwt.exceptions import PyJWTError
from core.settings import settings

def decode_token(token):
    try:
        return jwt.decode(jwt=token, key=settings.ACCESS_JWT_SECRET, algorithms=['HS256'])
    except PyJWTError:
        return "Error"