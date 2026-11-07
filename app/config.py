import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    APP_NAME: str = "OpenSite — SEO & Conversion Intelligence"
    APP_VERSION: str = "1.0.0"
    HINDSIGHT_BASE_URL: str = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
    HINDSIGHT_API_KEY: str = os.getenv("HINDSIGHT_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "qwen/qwen3-32b")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    PORT: int = int(os.getenv("PORT", "8000"))
    UI_PORT: int = int(os.getenv("UI_PORT", "8501"))
    OPENSITE_SITES_PATH: str = os.getenv("OPENSITE_SITES_PATH", "")

settings = Settings()
