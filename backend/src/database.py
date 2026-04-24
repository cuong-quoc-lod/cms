import ssl
from pymongo import MongoClient
from pymongo.database import Database
from src.config import MONGO_URI, MONGO_DB_NAME

_client: MongoClient | None = None
_db: Database | None = None


def get_db() -> Database:
    """Return the shared database instance, creating it on first call."""
    global _client, _db
    if _db is None:
        _client = MongoClient(
            MONGO_URI,
            tls=True,
            tlsInsecure=True,
        )
        _db = _client[MONGO_DB_NAME]
    return _db


def close_db() -> None:
    """Close the MongoDB connection."""
    global _client, _db
    if _client is not None:
        _client.close()
        _client = None
        _db = None

