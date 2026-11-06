from __future__ import annotations

from fastapi import APIRouter

from app.schemas.schemas import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Return API health status."""
    return HealthResponse(status="ok", version="1.0.0")
