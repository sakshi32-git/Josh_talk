from __future__ import annotations

"""Business logic for creating and running evaluation runs."""

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import EvaluationRun, Recording, Score
from app.evaluation import scorer as scorer_module


# Directory where hypothesis RTTM files are persisted
HYPOTHESIS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "hypotheses"


async def create_evaluation_run(
    db: AsyncSession,
    model_id: str,
    recording_id: str,
    hypothesis_rttm_path: str,
    collar: float = 0.25,
    score_overlap: bool = True,
) -> EvaluationRun:
    """Persist a new EvaluationRun row (status=pending) and return it."""
    run = EvaluationRun(
        id=str(uuid.uuid4()),
        model_id=model_id,
        recording_id=recording_id,
        status="pending",
        collar=collar,
        score_overlap=score_overlap,
        hypothesis_rttm_path=hypothesis_rttm_path,
        created_at=datetime.now(timezone.utc),
    )
    db.add(run)
    await db.commit()
    await db.refresh(run)
    return run


async def run_evaluation(
    db: AsyncSession,
    run_id: str,
) -> EvaluationRun:
    """Execute scoring for the given run_id and update the row.

    1. Loads the EvaluationRun and its associated Recording.
    2. Calls scorer.score(reference_rttm, hypothesis_rttm, ...).
    3. Persists results (or error) back to the DB.
    4. Returns the updated EvaluationRun.
    """
    # Fetch run
    result = await db.execute(select(EvaluationRun).where(EvaluationRun.id == run_id))
    run: EvaluationRun | None = result.scalar_one_or_none()
    if run is None:
        raise ValueError(f"EvaluationRun {run_id} not found.")

    # Fetch recording for reference path
    result_rec = await db.execute(
        select(Recording).where(Recording.id == run.recording_id)
    )
    recording: Recording | None = result_rec.scalar_one_or_none()
    if recording is None:
        run.status = "failed"
        run.error_message = f"Recording {run.recording_id} not found."
        run.completed_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(run)
        return run

    if not recording.reference_rttm_path:
        run.status = "failed"
        run.error_message = "Recording has no reference RTTM path set."
        run.completed_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(run)
        return run

    # Mark as running
    run.status = "running"
    await db.commit()

    start_time = datetime.now(timezone.utc)

    try:
        metrics: dict[str, Any] = scorer_module.score(
            reference_rttm_path=recording.reference_rttm_path,
            hypothesis_rttm_path=run.hypothesis_rttm_path,
            collar=run.collar,
            skip_overlap=not run.score_overlap,
        )

        end_time = datetime.now(timezone.utc)
        runtime = (end_time - start_time).total_seconds()

        run.status = "completed"
        run.der = metrics["der"]
        run.jer = metrics["jer"]
        run.miss_rate = metrics["miss_rate"]
        run.false_alarm_rate = metrics["false_alarm_rate"]
        run.confusion_rate = metrics["confusion_rate"]
        run.reference_duration = metrics["reference_duration"]
        run.runtime_seconds = runtime
        run.completed_at = end_time

        # Persist individual Score rows
        metric_names = ["der", "jer", "miss_rate", "false_alarm_rate", "confusion_rate"]
        for mname in metric_names:
            score_row = Score(
                id=str(uuid.uuid4()),
                run_id=run.id,
                metric_name=mname,
                value=metrics[mname],
            )
            db.add(score_row)

    except Exception as exc:  # noqa: BLE001
        end_time = datetime.now(timezone.utc)
        run.status = "failed"
        run.error_message = str(exc)
        run.completed_at = end_time
        run.runtime_seconds = (end_time - start_time).total_seconds()

    await db.commit()
    await db.refresh(run)
    return run
