from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "User Service API"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000
