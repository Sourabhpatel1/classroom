from fastapi import APIRouter, Depends, HTTPException, Body, Response, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from core.security import create_access_token, create_refresh_token
from core.settings import settings
from .helpers import authenticate_user, refresh_access_token


token_router = APIRouter()

@token_router.post("/")
async def generate_token(form_data:OAuth2PasswordRequestForm =Depends()):

    try:
        user = await authenticate_user(email=form_data.username, password=form_data.password)
    except:
        raise HTTPException(status_code=400, detail=f"User with the email {form_data.username} is not registered please register!!!")
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials", headers={"WWW-Authenticate": "Bearer"},)

    email = user.email

    payload = email

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)
    # response.set_cookie( 
    #     key="access_token", 
    #     value=str(access_token), 
    #     httponly=True, 
    #     max_age=settings.ACCESS_TOKEN_EXPIRE_DELTA, 
    #     expires=settings.ACCESS_TOKEN_EXPIRE_DELTA,
    #     samesite='none',
    #     domain="http://localhost:5173"
    # )
    # response.set_cookie(
    #     key="refresh_token", 
    #     value=refresh_token, 
    #     httponly=True, 
    #     max_age=settings.REFRESH_TOKEN_EXPIRE_DELTA, 
    #     expires=settings.REFRESH_TOKEN_EXPIRE_DELTA,
    #     samesite='none',
    #     domain="http://localhost:5173"
    # )
    response = JSONResponse(content={"message":"ok"})
    response.set_cookie(key="access_token", value=access_token, secure=True, httponly=True, samesite="none", expires=settings.ACCESS_TOKEN_EXPIRE_DELTA, max_age=settings.ACCESS_TOKEN_EXPIRE_DELTA)
    response.set_cookie(key="refresh_token", value=refresh_token, secure=True, httponly=True, samesite="none", expires=settings.REFRESH_TOKEN_EXPIRE_DELTA, max_age=settings.REFRESH_TOKEN_EXPIRE_DELTA)
    return response


@token_router.post("/refresh")
def refresh_tokens(request:Request, response:Response):
    try:
        _refresh_token = request.cookies.get("refresh_token")
        print(_refresh_token)
        access_token, refresh_token = refresh_access_token(refresh_token=_refresh_token)
       
        response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=settings.ACCESS_TOKEN_EXPIRE_DELTA, expires=settings.ACCESS_TOKEN_EXPIRE_DELTA)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=settings.REFRESH_TOKEN_EXPIRE_DELTA, expires=settings.REFRESH_TOKEN_EXPIRE_DELTA)

        return {"Meessage" : "Token Refreshed Succesfully"}
    except:
        raise HTTPException(
            status_code=400,
            detail="Bad Request"
        )
