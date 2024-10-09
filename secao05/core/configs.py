from pydantic import BaseSettings
 
class Settings(BaseSettings):
    API_V_STR:str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://faustinok:1234@localhost:5432/api_test'
    class Config:
        case_sensitive = True

settings: Settings = Settings()