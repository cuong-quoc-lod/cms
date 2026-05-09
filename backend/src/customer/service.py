from typing import Optional
from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

from src.customer.repository import CustomerRepository
from src.customer.schemas import (
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerResponse,
    CustomerListResponse,
)


class CustomerService:
    def __init__(self, repo: CustomerRepository):
        self.repo = repo

    # ── Helpers ────────────────────────────────────────────────────────────────

    @staticmethod
    def _to_response(doc: dict) -> CustomerResponse:
        return CustomerResponse(**doc)

    # ── Business logic ─────────────────────────────────────────────────────────

    def get_customers(
        self,
        *,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> CustomerListResponse:
        docs, total = self.repo.find_all(
            search=search,
            is_active=is_active,
            page=page,
            page_size=page_size,
        )
        return CustomerListResponse(
            total=total,
            page=page,
            page_size=page_size,
            customers=[self._to_response(d) for d in docs],
        )

    def get_customer_by_id(self, customer_id: str) -> CustomerResponse:
        doc = self.repo.find_by_id(customer_id)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer '{customer_id}' not found.",
            )
        return self._to_response(doc)

    def create_customer(self, payload: CustomerCreateRequest) -> CustomerResponse:
        # Check duplicate email
        existing = self.repo.find_by_email(payload.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{payload.email}' already registered.",
            )
        try:
            doc = self.repo.create(payload.model_dump(exclude_none=False))
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{payload.email}' already registered.",
            )
        return self._to_response(doc)

    def update_customer(
        self, customer_id: str, payload: CustomerUpdateRequest
    ) -> CustomerResponse:
        # Ensure customer exists
        self.get_customer_by_id(customer_id)

        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update.",
            )

        # Check new email uniqueness
        if "email" in update_data:
            existing = self.repo.find_by_email(update_data["email"])
            if existing and existing["id"] != customer_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Email '{update_data['email']}' is already in use.",
                )

        doc = self.repo.update(customer_id, update_data)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer '{customer_id}' not found.",
            )
        return self._to_response(doc)

    def delete_customer(self, customer_id: str) -> dict:
        """Soft-delete: marks customer as inactive."""
        self.get_customer_by_id(customer_id)
        deleted = self.repo.delete(customer_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete customer.",
            )
        return {"message": f"Customer '{customer_id}' has been deactivated."}
