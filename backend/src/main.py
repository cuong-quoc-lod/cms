from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.config import ALLOWED_ORIGINS, RATE_LIMIT_PER_MINUTE, APP_ENV
from src.database import get_db, close_db
from src.health.router import router as health_router
from src.auth.router import router as auth_router
from src.customer.router import router as customer_router

# ── Rate limiter ───────────────────────────────────────────────────────────────
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[RATE_LIMIT_PER_MINUTE],
)

# ── App factory ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="CMS API",
    description="Customer Management System REST API",
    version="1.0.0",
    docs_url="/docs" if APP_ENV != "production" else None,
    redoc_url="/redoc" if APP_ENV != "production" else None,
)

# State & error handler for slowapi
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── Middleware ─────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Lifecycle ──────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    """Initialise DB connection on startup."""
    get_db()
    print("[OK] Connected to MongoDB")


@app.on_event("shutdown")
async def shutdown_event():
    """Close DB connection gracefully on shutdown."""
    close_db()
    print("[OFF] MongoDB connection closed")


# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(customer_router)


# ── Root redirect ──────────────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    return {"message": "CMS API is running. Visit /docs for documentation."}
