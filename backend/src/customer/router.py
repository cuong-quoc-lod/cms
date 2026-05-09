from typing import Optional
from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import JSONResponse

from src.customer.schemas import (
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerResponse,
    CustomerListResponse,
)
from src.customer.service import CustomerService
from src.customer.repository import CustomerRepository
from src.database import get_db
from src.dependencies import get_current_user_id


router = APIRouter(prefix="/api/customer", tags=["Customer"])


# ── Dependency injection ────────────────────────────────────────────────────────

def get_customer_service() -> CustomerService:
    db = get_db()
    repo = CustomerRepository(db)
    return CustomerService(repo)


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get(
    "",
    response_model=CustomerListResponse,
    summary="List / search customers",
    description=(
        "Returns a paginated list of customers. "
        "Supports full-text search on name, email, and phone."
    ),
)
def list_customers(
    request: Request,
    search: Optional[str] = Query(None, description="Search by name, email, or phone"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    service: CustomerService = Depends(get_customer_service),
    _user_id: str = Depends(get_current_user_id),
) -> CustomerListResponse:
    return service.get_customers(
        search=search,
        is_active=is_active,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
    summary="Get a customer by ID",
)
def get_customer(
    customer_id: str,
    service: CustomerService = Depends(get_customer_service),
    _user_id: str = Depends(get_current_user_id),
) -> CustomerResponse:
    return service.get_customer_by_id(customer_id)


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new customer",
)
def create_customer(
    payload: CustomerCreateRequest,
    service: CustomerService = Depends(get_customer_service),
    _user_id: str = Depends(get_current_user_id),
) -> CustomerResponse:
    return service.create_customer(payload)


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
    summary="Update an existing customer",
)
def update_customer(
    customer_id: str,
    payload: CustomerUpdateRequest,
    service: CustomerService = Depends(get_customer_service),
    _user_id: str = Depends(get_current_user_id),
) -> CustomerResponse:
    return service.update_customer(customer_id, payload)


@router.delete(
    "/{customer_id}",
    summary="Soft-delete a customer (deactivate)",
    status_code=status.HTTP_200_OK,
)
def delete_customer(
    customer_id: str,
    service: CustomerService = Depends(get_customer_service),
    _user_id: str = Depends(get_current_user_id),
) -> dict:
    return service.delete_customer(customer_id)
