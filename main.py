from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes import base_router
import uvicorn
import os

def create_database():
    Base.metadata.create_all(bind=engine)

def create_app():
    create_database()
    app = FastAPI()
    app.include_router(base_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins = ["https://calssroom-front-production.up.railway.app"],
        allow_credentials=True,
        allow_methods=["GET","POST","PUT","DELETE"],
        allow_headers=["Access-Control-Allow-Headers", "Content-Type", "Authorization", "Access-Control-Allow-Origin", "Set-Cookie"]
        )
    return app

app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=os.getenv("PORT", default=5000), log_level="info")