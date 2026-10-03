import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # DeepSeek
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
    
    # Server
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
    
    # Models
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MODEL = os.getenv("MODEL", "deepseek-chat")
    REASONING_MODEL = os.getenv("REASONING_MODEL", "deepseek-reasoner")
    REASONING_MAX_TOKENS = int(os.getenv("REASONING_MAX_TOKENS", "8000"))
    
    # Features
    ENABLE_REASONING = os.getenv("ENABLE_REASONING", "true").lower() == "true"
    ENABLE_CONTEXT = os.getenv("ENABLE_CONTEXT", "true").lower() == "true"
    MAX_HISTORY = int(os.getenv("MAX_HISTORY", "20"))
    CONTEXT_TIMEOUT = int(os.getenv("CONTEXT_TIMEOUT", "3600"))
    
    # Redis
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))
    REDIS_ENABLED = os.getenv("REDIS_ENABLED", "false").lower() == "true"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
