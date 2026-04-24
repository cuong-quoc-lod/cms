import uvicorn
from src.config import APP_HOST, APP_PORT, APP_ENV

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=APP_HOST,
        port=APP_PORT,
        reload=APP_ENV != "production",
        log_level="info",
    )
