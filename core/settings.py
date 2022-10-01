
class Settings:
    DATABASE_URL:str = "sqlite:///./app.db"
    ACCESS_JWT_SECRET = '$2b$12$qtyydfBnYRGMwRH4R2HeVOliufDgKwE5cSySklIUWDoKa7/2ZI9mK'
    REFRESH_JWT_SECRET = '$2b$12$qtyydfBnYRGMwRH4R2HeVOliufDgKwE5cSySklIUWDoKaldkjskd'
    ACCESS_TOKEN_EXPIRE_DELTA = 15
    REFRESH_TOKEN_EXPIRE_DELTA = 3600*24*7
    EXPIRE_TIME_DELTA = 15*60

settings = Settings()