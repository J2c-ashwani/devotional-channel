import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STORAGE_DIR = BASE_DIR / "storage"
CONFIG_DIR = BASE_DIR / "config"

class Settings(BaseSettings):
    APP_NAME: str = "Pauranik Gatha - Autonomous YouTube Studio"
    ENV: str = "development"
    DEBUG: bool = True
    
    # Base paths
    BASE_DIR: Path = BASE_DIR
    STORAGE_DIR: Path = STORAGE_DIR
    CONFIG_DIR: Path = CONFIG_DIR
    
    # Database
    DATABASE_URL: str = f"sqlite+aiosqlite:///{STORAGE_DIR}/pauranik_studio.db"
    
    # YouTube API Credentials
    YOUTUBE_CLIENT_ID: str = "mock_client_id"
    YOUTUBE_CLIENT_SECRET: str = "mock_client_secret"
    YOUTUBE_REFRESH_TOKEN: str = "mock_refresh_token"
    YOUTUBE_CHANNEL_ID: str = "UC_CINEMATIC_MYTHOLOGY_HINDI"
    
    # AI API Keys (Configurable via environment variables)
    GEMINI_API_KEY: str = ""
    GOOGLE_CLOUD_PROJECT: str = ""
    GOOGLE_CLOUD_LOCATION: str = "us-central1"
    GOOGLE_APPLICATION_CREDENTIALS: str = ""
    OPENAI_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""
    IMAGE_GEN_PROVIDER: str = "modular_gemini"  # "modular_gemini", "mock", "flux"
    VIDEO_GEN_PROVIDER: str = "modular_motion"  # "modular_motion", "mock"
    TTS_PROVIDER: str = "edge_tts"             # "edge_tts", "elevenlabs", "mock"
    
    # Cost & Budget Guardrails (Monthly limit in USD)
    MONTHLY_BUDGET_USD: float = 150.0
    COST_ALERT_THRESHOLD_PCT: float = 80.0
    EMERGENCY_KILL_SWITCH: bool = False
    
    # Quality Assurance Thresholds
    MINIMUM_QC_SCORE: int = 90
    FAIL_CLOSED: bool = True
    
    # Timezone
    PUBLISH_TIMEZONE: str = "Asia/Kolkata"
    
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
