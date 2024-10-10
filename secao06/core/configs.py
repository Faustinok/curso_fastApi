from typing import List
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V_STR:str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://faustinok:1234@localhost:5432/api_test'
    DbBaseModel = declarative_base()
    JWT_SECRET: str = 'Ko8MG9JKdYOIlxvDtDh3pIBHkmdyBLcggxWOfP388u0'
    """
    import secrets 
    token: str = secrets.token_urlsafe(32)
    """

    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 60 * 24 * 7

    class Config:
        case_sensitive = True

settings: Settings = Settings()
