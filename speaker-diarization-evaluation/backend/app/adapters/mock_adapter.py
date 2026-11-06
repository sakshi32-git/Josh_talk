from __future__ import annotations

"""Mock diarization adapter for testing.

Reads a pre-existing RTTM file and returns its segments as the diarization
output – useful for integration tests that do not need a real model.
"""

import os
from pathlib import Path

from app.adapters.base import DiarizationAdapter
from app.evaluation.rttm import parse_rttm


class MockAdapter(DiarizationAdapter):
    """Adapter that reads a pre-existing RTTM file and returns its segments."""

    name = "mock"
    version = "1.0"
    provider = "Local"

    def __init__(self, hypothesis_rttm_path: str) -> None:
        self.hypothesis_rttm_path = hypothesis_rttm_path

    def diarize(self, audio_path: str) -> dict:
        """Return segments from the pre-existing hypothesis RTTM.

        ``audio_path`` is accepted but not used; the RTTM path provided
        at construction time is used instead.
        """
        try:
            filepath = Path(self.hypothesis_rttm_path)
            if not filepath.exists():
                raise FileNotFoundError(
                    f"Mock RTTM file not found: {self.hypothesis_rttm_path}"
                )

            raw_segments = parse_rttm(filepath)

            # Normalise to the standard output schema
            segments = [
                {
                    "start": seg["start"],
                    "end": seg["end"],
                    "speaker": seg["speaker"],
                }
                for seg in raw_segments
            ]

            # Derive a recording_id from the first segment or the filename
            if raw_segments:
                recording_id = raw_segments[0]["recording_id"]
            else:
                recording_id = filepath.stem

            return {
                "recording_id": recording_id,
                "segments": segments,
                "model": self.name,
                "version": self.version,
                "status": "completed",
                "error": None,
            }

        except Exception as exc:  # noqa: BLE001
            return {
                "recording_id": "",
                "segments": [],
                "model": self.name,
                "version": self.version,
                "status": "failed",
                "error": str(exc),
            }
