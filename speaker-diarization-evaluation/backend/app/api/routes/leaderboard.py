from __future__ import annotations

"""Leaderboard API route."""

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import EvaluationRun, Model, Recording
from app.schemas.schemas import LeaderboardEntry

router = APIRouter(tags=["Leaderboard"])


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
async def get_leaderboard(
    dataset_id: Optional[str] = None,
    min_speakers: Optional[int] = None,
    max_speakers: Optional[int] = None,
    condition: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> list[LeaderboardEntry]:
    """Return aggregated per-model statistics.

    Query params:
        dataset_id: Filter by dataset.
        min_speakers: Minimum number of speakers in the recording.
        max_speakers: Maximum number of speakers in the recording.
        condition: Recording condition (clean / noisy / overlapping).
    """
    # Fetch all models
    models_result = await db.execute(select(Model))
    all_models = models_result.scalars().all()

    # Build recording filter set if needed
    filtered_recording_ids: set[str] | None = None
    if any(p is not None for p in [dataset_id, min_speakers, max_speakers, condition]):
        rec_query = select(Recording)
        if dataset_id is not None:
            rec_query = rec_query.where(Recording.dataset_id == dataset_id)
        if min_speakers is not None:
            rec_query = rec_query.where(Recording.num_speakers >= min_speakers)
        if max_speakers is not None:
            rec_query = rec_query.where(Recording.num_speakers <= max_speakers)
        if condition is not None:
            rec_query = rec_query.where(Recording.condition == condition)
        recs_result = await db.execute(rec_query)
        filtered_recording_ids = {r.id for r in recs_result.scalars().all()}

    # Fetch all runs
    runs_result = await db.execute(select(EvaluationRun))
    all_runs = runs_result.scalars().all()

    # Group by model
    entries: list[LeaderboardEntry] = []
    for model in all_models:
        model_runs = [r for r in all_runs if r.model_id == model.id]
        if filtered_recording_ids is not None:
            model_runs = [r for r in model_runs if r.recording_id in filtered_recording_ids]

        completed = [r for r in model_runs if r.status == "completed"]
        failed = [r for r in model_runs if r.status == "failed"]

        def _avg(values: list) -> Optional[float]:
            vals = [v for v in values if v is not None]
            return round(sum(vals) / len(vals), 4) if vals else None

        entry = LeaderboardEntry(
            model_id=model.id,
            model_name=model.name,
            provider=model.provider,
            version=model.version,
            avg_der=_avg([r.der for r in completed]),
            avg_jer=_avg([r.jer for r in completed]),
            avg_miss=_avg([r.miss_rate for r in completed]),
            avg_false_alarm=_avg([r.false_alarm_rate for r in completed]),
            avg_confusion=_avg([r.confusion_rate for r in completed]),
            num_recordings=len(set(r.recording_id for r in model_runs)),
            num_failed=len(failed),
            avg_runtime=_avg([r.runtime_seconds for r in completed]),
        )
        entries.append(entry)

    # Sort by avg_der ascending (None last)
    entries.sort(key=lambda e: (e.avg_der is None, e.avg_der or 0))
    return entries
