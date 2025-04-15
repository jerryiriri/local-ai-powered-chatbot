from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Local AI Chatbot"
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "llama3"
    DATABASE_URL: str = "sqlite:///./chat_history.db"

    class Config:
        env_file = ".env"

settings = Settings()
