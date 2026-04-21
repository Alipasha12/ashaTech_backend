from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SMTP_SERVER: str | None = None
    SMTP_PORT: int = 587
    EMAIL_ADDRESS: str | None = None
    EMAIL_PASSWORD: str | None = None
    SECRET_KEY: str = "dev-secret"
    REFRESH_SECRET_KEY: str = "dev-refresh-secret"
    PORT: int = 8000
    REFRESH_TOKEN_EXPIRE_MINUTES: int  
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    model_config = SettingsConfigDict(env_file=".env",extra="allow")
settings = Settings()