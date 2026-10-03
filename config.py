import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """Application configuration settings"""
    
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # DeepSeek Configuration
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_URL: str = os.getenv(
        "DEEPSEEK_API_URL", 
        "https://api.deepseek.com/v1/chat/completions"
    )
    
    # Server Configuration
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")
    
    # Model Configuration
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    MODEL: str = os.getenv("MODEL", "deepseek-chat")
    REASONING_MODEL: str = os.getenv("REASONING_MODEL", "deepseek-reasoner")
    REASONING_MAX_TOKENS: int = int(os.getenv("REASONING_MAX_TOKENS", "8000"))
    
    # Redis Configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "true").lower() == "true"
    
    # Features
    ENABLE_REASONING: bool = os.getenv("ENABLE_REASONING", "true").lower() == "true"
    ENABLE_CONTEXT: bool = os.getenv("ENABLE_CONTEXT", "true").lower() == "true"
    MAX_HISTORY: int = int(os.getenv("MAX_HISTORY", "20"))
    CONTEXT_TIMEOUT: int = int(os.getenv("CONTEXT_TIMEOUT", "3600"))  # 1 hour
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
