from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId
from pymongo.database import Database
from pymongo import ASCENDING, DESCENDING
import re

COLLECTION = "customers"


# ── Helpers ────────────────────────────────────────────────────────────────────

def _doc_to_dict(doc: dict) -> dict:
    """Convert a MongoDB document to a serialisable dict."""
    doc["id"] = str(doc.pop("_id"))
    return doc


def _build_filter(
    search: Optional[str],
    is_active: Optional[bool],
) -> dict:
    query: dict = {}
    if is_active is not None:
        query["is_active"] = is_active
    if search:
        safe_search = re.escape(search)
        query["$or"] = [
            {"name": {"$regex": safe_search, "$options": "i"}},
            {"email": {"$regex": safe_search, "$options": "i"}},
            {"phone": {"$regex": safe_search, "$options": "i"}},
        ]
    return query


# ── Repository ─────────────────────────────────────────────────────────────────

class CustomerRepository:
    def __init__(self, db: Database):
        self.col = db[COLLECTION]
        # Ensure unique index on email
        try:
            self.col.create_index([("email", ASCENDING)], unique=True)
        except Exception:
            pass

    # ---------- Read ----------

    def find_all(
        self,
        *,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "created_at",
        sort_order: int = DESCENDING,
    ) -> tuple[list[dict], int]:
        query = _build_filter(search, is_active)
        total = self.col.count_documents(query)
        skip = (page - 1) * page_size
        cursor = (
            self.col.find(query)
            .sort(sort_by, sort_order)
            .skip(skip)
            .limit(page_size)
        )
        docs = [_doc_to_dict(doc) for doc in cursor]
        return docs, total

    def find_by_id(self, customer_id: str) -> Optional[dict]:
        try:
            oid = ObjectId(customer_id)
        except Exception:
            return None
        doc = self.col.find_one({"_id": oid})
        return _doc_to_dict(doc) if doc else None

    def find_by_email(self, email: str) -> Optional[dict]:
        doc = self.col.find_one({"email": email})
        return _doc_to_dict(doc) if doc else None

    # ---------- Write ----------

    def create(self, data: dict) -> dict:
        now = datetime.now(timezone.utc)
        document = {
            **data,
            "is_active": data.get("is_active", True),
            "created_at": now,
            "updated_at": now,
        }
        result = self.col.insert_one(document)
        document["_id"] = result.inserted_id
        return _doc_to_dict(document)

    def update(self, customer_id: str, data: dict) -> Optional[dict]:
        try:
            oid = ObjectId(customer_id)
        except Exception:
            return None
        update_data = {k: v for k, v in data.items() if v is not None}
        update_data["updated_at"] = datetime.now(timezone.utc)
        self.col.update_one({"_id": oid}, {"$set": update_data})
        return self.find_by_id(customer_id)

    def delete(self, customer_id: str) -> bool:
        """Soft delete: set is_active = False."""
        try:
            oid = ObjectId(customer_id)
        except Exception:
            return False
        result = self.col.update_one(
            {"_id": oid},
            {"$set": {"is_active": False, "updated_at": datetime.now(timezone.utc)}},
        )
        return result.modified_count > 0

    def hard_delete(self, customer_id: str) -> bool:
        try:
            oid = ObjectId(customer_id)
        except Exception:
            return False
        result = self.col.delete_one({"_id": oid})
        return result.deleted_count > 0
