from __future__ import annotations

"""PyAnnote speaker diarization adapter.

Requires a valid HuggingFace auth token and acceptance of the pyannote model
usage terms. When the model is unavailable the adapter gracefully returns a
``"failed"`` status with an informative error message so the rest of the
platform continues to function.
"""

import os
from pathlib import Path

from app.adapters.base import DiarizationAdapter


class PyAnnoteAdapter(DiarizationAdapter):
    """Adapter for pyannote/speaker-diarization-3.1."""

    name = "pyannote/speaker-diarization-3.1"
    version = "3.1"
    provider = "pyannote.audio"

    def __init__(self, auth_token: str | None = None) -> None:
        self.auth_token = auth_token or os.getenv("HUGGINGFACE_TOKEN")
        self._pipeline = None

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _load_pipeline(self) -> None:
        """Lazily load the pyannote pipeline on first use."""
        try:
            from pyannote.audio import Pipeline  # type: ignore[import]

            self._pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=self.auth_token,
            )
        except ImportError as exc:
            raise RuntimeError(
                "pyannote.audio is not installed. "
                "Install it with: pip install pyannote.audio"
            ) from exc
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                f"Failed to load pyannote pipeline: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def diarize(self, audio_path: str) -> dict:
        """Run speaker diarization using pyannote/speaker-diarization-3.1.

        Args:
            audio_path: Path to the audio file (WAV, 16 kHz mono recommended).

        Returns:
            Standard adapter output dict.
        """
        audio_path_obj = Path(audio_path)
        recording_id = audio_path_obj.stem

        try:
            if self._pipeline is None:
                self._load_pipeline()

            diarization = self._pipeline(str(audio_path_obj))

            segments = []
            for segment, _, speaker in diarization.itertracks(yield_label=True):
                segments.append(
                    {
                        "start": round(segment.start, 6),
                        "end": round(segment.end, 6),
                        "speaker": speaker,
                    }
                )

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
                "recording_id": recording_id,
                "segments": [],
                "model": self.name,
                "version": self.version,
                "status": "failed",
                "error": str(exc),
            }
