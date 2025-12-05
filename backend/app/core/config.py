from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Interview Agent"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./interview_agent.db"
    
    # Security
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE" # Change this in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_BASE: Optional[str] = None # For compatible APIs like SambaNova, Groq, etc.
    OPENAI_MODEL_NAME: str = "gpt-3.5-turbo" # Default model, can be overridden

    class Config:
        env_file = ".env"

settings = Settings()
# Reload trigger - Key Updated - Force Reload
