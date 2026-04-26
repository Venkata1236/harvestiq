from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # App
    ENV: str = "development"
    LOG_LEVEL: str = "DEBUG"

    # Groq
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama3-70b-8192"

    # Database
    DATABASE_URL: str

    # Model
    MODEL_PATH: str = "saved_models/harvestiq_resnet50.pt"
    CLASS_NAMES_PATH: str = "saved_models/class_names.json"
    CONFIDENCE_THRESHOLD: float = 0.65

    # ChromaDB
    CHROMA_DB_PATH: str = "chroma_db/"

    # Derived paths (computed from MODEL_PATH)
    @property
    def model_full_path(self) -> Path:
        return Path(self.MODEL_PATH)

    @property
    def class_names_full_path(self) -> Path:
        return Path(self.CLASS_NAMES_PATH)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()