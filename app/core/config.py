from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGO_URL: str
    APP_TITLE: str = "Rule Engine API"
    APP_VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"

settings = Settings()
