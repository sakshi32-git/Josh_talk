from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Boolean,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _new_uuid() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True, default=_new_uuid)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    language = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)

    recordings = relationship("Recording", back_populates="dataset", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# Recording
# ---------------------------------------------------------------------------


class Recording(Base):
    __tablename__ = "recordings"

    id = Column(String, primary_key=True, default=_new_uuid)
    dataset_id = Column(String, ForeignKey("datasets.id", ondelete="SET NULL"), nullable=True)
    filename = Column(String, nullable=False)
    duration_seconds = Column(Float, nullable=True)
    sample_rate = Column(Integer, nullable=True)
    channels = Column(Integer, nullable=True, default=1)
    condition = Column(String, nullable=True)  # clean / noisy / overlapping
    num_speakers = Column(Integer, nullable=True)
    reference_rttm_path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)

    dataset = relationship("Dataset", back_populates="recordings")
    evaluation_runs = relationship("EvaluationRun", back_populates="recording", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------


class Model(Base):
    __tablename__ = "models"

    id = Column(String, primary_key=True, default=_new_uuid)
    name = Column(String, nullable=False)
    provider = Column(String, nullable=True)
    version = Column(String, nullable=True)
    model_type = Column(String, nullable=True)   # open_source / commercial / api
    run_method = Column(String, nullable=True)   # local / api / docker
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)

    evaluation_runs = relationship("EvaluationRun", back_populates="model", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# EvaluationRun
# ---------------------------------------------------------------------------


class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id = Column(String, primary_key=True, default=_new_uuid)
    model_id = Column(String, ForeignKey("models.id", ondelete="CASCADE"), nullable=False)
    recording_id = Column(String, ForeignKey("recordings.id", ondelete="CASCADE"), nullable=False)

    # Status
    status = Column(String, nullable=False, default="pending")  # pending/running/completed/failed/timed_out

    # Metrics
    der = Column(Float, nullable=True)
    jer = Column(Float, nullable=True)
    miss_rate = Column(Float, nullable=True)
    false_alarm_rate = Column(Float, nullable=True)
    confusion_rate = Column(Float, nullable=True)
    reference_duration = Column(Float, nullable=True)

    # Scoring parameters
    collar = Column(Float, nullable=False, default=0.25)
    score_overlap = Column(Boolean, nullable=False, default=True)

    # Runtime
    runtime_seconds = Column(Float, nullable=True)

    # Error / output
    error_message = Column(Text, nullable=True)
    raw_output_path = Column(String, nullable=True)
    hypothesis_rttm_path = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    model = relationship("Model", back_populates="evaluation_runs")
    recording = relationship("Recording", back_populates="evaluation_runs")
    scores = relationship("Score", back_populates="run", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# Score
# ---------------------------------------------------------------------------


class Score(Base):
    __tablename__ = "scores"

    id = Column(String, primary_key=True, default=_new_uuid)
    run_id = Column(String, ForeignKey("evaluation_runs.id", ondelete="CASCADE"), nullable=False)
    metric_name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)

    run = relationship("EvaluationRun", back_populates="scores")
