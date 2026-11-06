from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------


class DatasetCreate(BaseModel):
    name: str
    description: Optional[str] = None
    language: Optional[str] = None


class DatasetRead(DatasetCreate):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Recording
# ---------------------------------------------------------------------------


class RecordingCreate(BaseModel):
    id: Optional[str] = None
    dataset_id: Optional[str] = None
    filename: str
    duration_seconds: Optional[float] = None
    sample_rate: Optional[int] = None
    channels: Optional[int] = 1
    condition: Optional[str] = None  # clean / noisy / overlapping
    num_speakers: Optional[int] = None
    reference_rttm_path: Optional[str] = None


class RecordingRead(RecordingCreate):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------


class ModelCreate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    name: str
    provider: Optional[str] = None
    version: Optional[str] = None
    model_type: Optional[str] = None   # open_source / commercial / api
    run_method: Optional[str] = None   # local / api / docker
    description: Optional[str] = None


class ModelRead(ModelCreate):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    id: str
    created_at: datetime


# ---------------------------------------------------------------------------
# EvaluationRun
# ---------------------------------------------------------------------------


class EvaluationRunCreate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model_id: str
    recording_id: str
    collar: float = 0.25
    score_overlap: bool = True


class EvaluationRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    id: str
    model_id: str
    recording_id: str
    status: str
    der: Optional[float] = None
    jer: Optional[float] = None
    miss_rate: Optional[float] = None
    false_alarm_rate: Optional[float] = None
    confusion_rate: Optional[float] = None
    reference_duration: Optional[float] = None
    collar: float
    score_overlap: bool
    runtime_seconds: Optional[float] = None
    error_message: Optional[str] = None
    raw_output_path: Optional[str] = None
    hypothesis_rttm_path: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class EvaluationRunStatus(BaseModel):
    id: str
    status: str
    error_message: Optional[str] = None


# ---------------------------------------------------------------------------
# Leaderboard
# ---------------------------------------------------------------------------


class LeaderboardEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    model_id: str
    model_name: str
    provider: Optional[str] = None
    version: Optional[str] = None
    avg_der: Optional[float] = None
    avg_jer: Optional[float] = None
    avg_miss: Optional[float] = None
    avg_false_alarm: Optional[float] = None
    avg_confusion: Optional[float] = None
    num_recordings: int = 0
    num_failed: int = 0
    avg_runtime: Optional[float] = None


# ---------------------------------------------------------------------------
# Score
# ---------------------------------------------------------------------------


class ScoreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    run_id: str
    metric_name: str
    value: float
    created_at: datetime


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


class HealthResponse(BaseModel):
    status: str
    version: str
