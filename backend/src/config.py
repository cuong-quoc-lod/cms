import os
from dotenv import load_dotenv

load_dotenv()

# Server settings
APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
APP_ENV: str = os.getenv("APP_ENV", "development")

# MongoDB settings
MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "cms_db")

# CORS settings
ALLOWED_ORIGINS: list[str] = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]

# Rate Limiting
RATE_LIMIT: str = os.getenv("RATE_LIMIT", "10000")
RATE_LIMIT_PER_MINUTE: str = f"{RATE_LIMIT}/minute"
