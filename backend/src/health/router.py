from fastapi import APIRouter
from src.database import get_db

router = APIRouter(prefix="/api/health", tags=["Health"])


@router.get("", summary="Health check", description="Returns server and database status.")
def health_check() -> dict:
    status = {"server": "ok", "database": "ok"}
    try:
        db = get_db()
        # ping command to verify connectivity
        db.client.admin.command("ping")
    except Exception as exc:
        status["database"] = f"error: {str(exc)}"

    overall = "healthy" if all(v == "ok" for v in status.values()) else "degraded"
    return {"status": overall, **status}
