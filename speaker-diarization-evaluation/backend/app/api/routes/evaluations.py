from __future__ import annotations

"""Evaluations and Recordings API routes."""

import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import EvaluationRun, Recording
from app.schemas.schemas import EvaluationRunRead, RecordingCreate, RecordingRead
from app.services.evaluation_service import create_evaluation_run, run_evaluation

router = APIRouter(tags=["Evaluations"])

# Directory where uploaded RTTM files are saved
HYPOTHESIS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "hypotheses"
HYPOTHESIS_DIR.mkdir(parents=True, exist_ok=True)


# ===========================================================================
# RECORDINGS
# ===========================================================================


@router.post("/recordings", response_model=RecordingRead, status_code=status.HTTP_201_CREATED)
async def create_recording(
    payload: RecordingCreate,
    db: AsyncSession = Depends(get_db),
) -> RecordingRead:
    """Register a recording in the catalog."""
    rec = Recording(
        id=payload.id or str(uuid.uuid4()),
        dataset_id=payload.dataset_id,
        filename=payload.filename,
        duration_seconds=payload.duration_seconds,
        sample_rate=payload.sample_rate,
        channels=payload.channels,
        condition=payload.condition,
        num_speakers=payload.num_speakers,
        reference_rttm_path=payload.reference_rttm_path,
    )
    db.add(rec)
    await db.commit()
    await db.refresh(rec)
    return RecordingRead.model_validate(rec)


@router.get("/recordings", response_model=list[RecordingRead])
async def list_recordings(
    db: AsyncSession = Depends(get_db),
) -> list[RecordingRead]:
    """List all recordings."""
    result = await db.execute(select(Recording).order_by(Recording.created_at.desc()))
    return [RecordingRead.model_validate(r) for r in result.scalars().all()]


# ===========================================================================
# EVALUATIONS
# ===========================================================================


@router.post("/evaluations", response_model=EvaluationRunRead, status_code=status.HTTP_201_CREATED)
async def create_evaluation(
    model_id: str = Form(...),
    recording_id: str = Form(...),
    collar: float = Form(0.25),
    score_overlap: bool = Form(True),
    hypothesis_rttm: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> EvaluationRunRead:
    """Submit a hypothesis RTTM, score it synchronously, return results."""
    # Save uploaded RTTM to disk
    run_id = str(uuid.uuid4())
    dest_path = HYPOTHESIS_DIR / f"{run_id}.rttm"
    contents = await hypothesis_rttm.read()
    dest_path.write_bytes(contents)

    # Create the run row
    run = await create_evaluation_run(
        db=db,
        model_id=model_id,
        recording_id=recording_id,
        hypothesis_rttm_path=str(dest_path),
        collar=collar,
        score_overlap=score_overlap,
    )

    # Score synchronously
    run = await run_evaluation(db=db, run_id=run.id)
    return EvaluationRunRead.model_validate(run)


@router.get("/evaluations", response_model=list[EvaluationRunRead])
async def list_evaluations(
    model_id: Optional[str] = None,
    recording_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> list[EvaluationRunRead]:
    """List all evaluation runs with optional filters."""
    query = select(EvaluationRun).order_by(EvaluationRun.created_at.desc())
    if model_id:
        query = query.where(EvaluationRun.model_id == model_id)
    if recording_id:
        query = query.where(EvaluationRun.recording_id == recording_id)

    result = await db.execute(query)
    return [EvaluationRunRead.model_validate(r) for r in result.scalars().all()]


@router.get("/evaluations/{run_id}", response_model=EvaluationRunRead)
async def get_evaluation(
    run_id: str,
    db: AsyncSession = Depends(get_db),
) -> EvaluationRunRead:
    """Get a single evaluation run by ID."""
    result = await db.execute(select(EvaluationRun).where(EvaluationRun.id == run_id))
    run: EvaluationRun | None = result.scalar_one_or_none()
    if run is None:
        raise HTTPException(status_code=404, detail=f"Evaluation run '{run_id}' not found.")
    return EvaluationRunRead.model_validate(run)


@router.post("/evaluations/{run_id}/retry", response_model=EvaluationRunRead)
async def retry_evaluation(
    run_id: str,
    db: AsyncSession = Depends(get_db),
) -> EvaluationRunRead:
    """Re-run scoring from the saved hypothesis RTTM for a given run."""
    result = await db.execute(select(EvaluationRun).where(EvaluationRun.id == run_id))
    run: EvaluationRun | None = result.scalar_one_or_none()
    if run is None:
        raise HTTPException(status_code=404, detail=f"Evaluation run '{run_id}' not found.")

    if not run.hypothesis_rttm_path or not Path(run.hypothesis_rttm_path).exists():
        raise HTTPException(
            status_code=422,
            detail="No saved hypothesis RTTM file found for this run.",
        )

    # Reset status to pending so run_evaluation picks it up
    run.status = "pending"
    run.error_message = None
    await db.commit()

    run = await run_evaluation(db=db, run_id=run_id)
    return EvaluationRunRead.model_validate(run)
