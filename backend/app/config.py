from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "CloudPulse Infrastructure Management"
    database_url: str = "postgresql+psycopg://cloudpulse_admin:cloudpulse_secure_pass_2026@localhost:5432/cloudpulse_db"
    environment: str = "production"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
