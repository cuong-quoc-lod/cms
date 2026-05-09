from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId
from pymongo import ASCENDING
from pymongo.database import Database

COLLECTION = "users"


def _doc_to_dict(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


class UserRepository:
    def __init__(self, db: Database):
        self.col = db[COLLECTION]
        # Unique index on username
        try:
            self.col.create_index([("username", ASCENDING)], unique=True)
        except Exception:
            pass

    # ---------- Read ----------

    def find_by_id(self, user_id: str) -> Optional[dict]:
        try:
            oid = ObjectId(user_id)
        except Exception:
            return None
        doc = self.col.find_one({"_id": oid})
        return _doc_to_dict(doc) if doc else None

    def find_by_username(self, username: str) -> Optional[dict]:
        doc = self.col.find_one({"username": username})
        return _doc_to_dict(doc) if doc else None

    # ---------- Write ----------

    def create(self, username: str, password_hash: str, full_name: Optional[str]) -> dict:
        now = datetime.now(timezone.utc)
        document = {
            "username": username,
            "password_hash": password_hash,
            "full_name": full_name,
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }
        result = self.col.insert_one(document)
        document["_id"] = result.inserted_id
        return _doc_to_dict(document)
