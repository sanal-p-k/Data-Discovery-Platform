from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database configuration
    database_url: str = "postgresql://postrges:Sanal.pk25@localhost:5432/mydatabase"
    database_echo: bool = False  # Set to True for SQL query logging

    # Authentication configuration
    secret_key: str = "your-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"  # Load environment variables from a .env file

# Create an instance of the settings
settings = Settings()