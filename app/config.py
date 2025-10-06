from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    MODEL_ID: str = "gpt-4o-mini"
    APP_BASE_URL: str = "http://localhost:8000"
    SCHEDULING_URL: str = "https://mychart.example.com/schedule"

    class Config:
        env_file = ".env"

settings = Settings()
