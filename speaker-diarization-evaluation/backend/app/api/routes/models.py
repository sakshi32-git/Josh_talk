from __future__ import annotations

import uuid
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import EvaluationRun, Model
from app.schemas.schemas import ModelCreate, ModelRead

router = APIRouter(tags=["Models"])


# ---------------------------------------------------------------------------
# POST /api/models
# ---------------------------------------------------------------------------


@router.post("/models", response_model=ModelRead, status_code=status.HTTP_201_CREATED)
async def create_model(
    payload: ModelCreate,
    db: AsyncSession = Depends(get_db),
) -> ModelRead:
    """Register a new diarization model."""
    model = Model(
        id=str(uuid.uuid4()),
        name=payload.name,
        provider=payload.provider,
        version=payload.version,
        model_type=payload.model_type,
        run_method=payload.run_method,
        description=payload.description,
    )
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return ModelRead.model_validate(model)


# ---------------------------------------------------------------------------
# GET /api/models
# ---------------------------------------------------------------------------


@router.get("/models", response_model=list[ModelRead])
async def list_models(
    db: AsyncSession = Depends(get_db),
) -> list[ModelRead]:
    """List all registered models."""
    result = await db.execute(select(Model).order_by(Model.created_at.desc()))
    models = result.scalars().all()
    return [ModelRead.model_validate(m) for m in models]


# ---------------------------------------------------------------------------
# GET /api/models/{id}
# ---------------------------------------------------------------------------


@router.get("/models/{model_id}", response_model=dict)
async def get_model(
    model_id: str,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Get a model by ID with aggregated evaluation statistics."""
    result = await db.execute(select(Model).where(Model.id == model_id))
    model: Model | None = result.scalar_one_or_none()
    if model is None:
        raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found.")

    # Fetch evaluation runs for this model
    runs_result = await db.execute(
        select(EvaluationRun).where(EvaluationRun.model_id == model_id)
    )
    runs = runs_result.scalars().all()

    completed = [r for r in runs if r.status == "completed"]
    failed = [r for r in runs if r.status == "failed"]

    def _avg(values: list[Optional[float]]) -> Optional[float]:
        vals = [v for v in values if v is not None]
        return round(sum(vals) / len(vals), 4) if vals else None

    per_recording = [
        {
            "run_id": r.id,
            "recording_id": r.recording_id,
            "status": r.status,
            "der": r.der,
            "jer": r.jer,
            "miss_rate": r.miss_rate,
            "false_alarm_rate": r.false_alarm_rate,
            "confusion_rate": r.confusion_rate,
            "runtime_seconds": r.runtime_seconds,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in runs
    ]

    return {
        "id": model.id,
        "name": model.name,
        "provider": model.provider,
        "version": model.version,
        "model_type": model.model_type,
        "run_method": model.run_method,
        "description": model.description,
        "created_at": model.created_at.isoformat() if model.created_at else None,
        "stats": {
            "num_runs": len(runs),
            "num_completed": len(completed),
            "num_failed": len(failed),
            "avg_der": _avg([r.der for r in completed]),
            "avg_jer": _avg([r.jer for r in completed]),
            "avg_miss": _avg([r.miss_rate for r in completed]),
            "avg_false_alarm": _avg([r.false_alarm_rate for r in completed]),
            "avg_confusion": _avg([r.confusion_rate for r in completed]),
            "avg_runtime": _avg([r.runtime_seconds for r in completed]),
        },
        "evaluation_runs": per_recording,
    }


# ---------------------------------------------------------------------------
# DELETE /api/models/{id}
# ---------------------------------------------------------------------------


@router.delete("/models/{model_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_model(
    model_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Delete a model by ID."""
    result = await db.execute(select(Model).where(Model.id == model_id))
    model: Model | None = result.scalar_one_or_none()
    if model is None:
        raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found.")
    await db.delete(model)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
