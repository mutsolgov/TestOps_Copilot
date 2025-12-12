from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TestOps Copilot"
    API_V1_STR: str = "/api/v1"
    
    AI_PROVIDER: str = "mock"
    OPENAI_API_KEY: str | None = None
    CLOUDRU_API_KEY: str | None = None
    
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
