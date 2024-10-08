from typing import List
from pydantic import BaseSettings, AnyHttpUrl
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    """
    Configuracoes gerais usadas na aplicacao
    """
    API_V_STR: str = '/api/v1/'
    DB_URL: str = 'postgresql+asyncpg://faustinok:1234@localhost:5432/api_test'
    DBBaseModel = declarative_base()
    
    class Config:
        case_sensitive = True


settings = Settings()
