import os


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self) -> None:
        self.app_name: str = os.getenv("APP_NAME", "ShiftInterview API")
        self.app_version: str = os.getenv("APP_VERSION", "0.1.0")
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite:///./shiftinterview.db")


settings = Settings()
