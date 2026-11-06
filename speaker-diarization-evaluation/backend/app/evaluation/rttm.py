from __future__ import annotations

"""RTTM parsing, writing, and conversion utilities.

RTTM line format:
  SPEAKER {recording_id} 1 {start:.3f} {duration:.3f} <NA> <NA> {speaker} <NA> <NA>
"""

from pathlib import Path
from typing import Any

from pyannote.core import Annotation, Segment


# ---------------------------------------------------------------------------
# Parse
# ---------------------------------------------------------------------------


def parse_rttm(filepath: str | Path) -> list[dict[str, Any]]:
    """Parse an RTTM file and return a list of segment dicts.

    Each dict has keys:
        recording_id (str), channel (int), start (float),
        duration (float), end (float), speaker (str)
    """
    filepath = Path(filepath)
    segments: list[dict[str, Any]] = []

    with filepath.open("r", encoding="utf-8") as fh:
        for lineno, raw_line in enumerate(fh, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            if len(parts) < 10:
                raise ValueError(
                    f"Line {lineno} in {filepath} has {len(parts)} fields; expected 10."
                )
            if parts[0].upper() != "SPEAKER":
                # skip non-SPEAKER lines (e.g., FILE or LEXEME types)
                continue

            recording_id = parts[1]
            channel = int(parts[2])
            start = float(parts[3])
            duration = float(parts[4])
            speaker = parts[7]

            segments.append(
                {
                    "recording_id": recording_id,
                    "channel": channel,
                    "start": start,
                    "duration": duration,
                    "end": round(start + duration, 6),
                    "speaker": speaker,
                }
            )

    return segments


# ---------------------------------------------------------------------------
# Write
# ---------------------------------------------------------------------------


def write_rttm(
    segments: list[dict[str, Any]],
    filepath: str | Path,
) -> None:
    """Write segments to an RTTM file.

    Each segment dict must have:
        recording_id (str), start (float), end (float), speaker (str)

    Optionally: channel (int, default 1)
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with filepath.open("w", encoding="utf-8") as fh:
        for seg in segments:
            recording_id = seg["recording_id"]
            channel = seg.get("channel", 1)
            start = float(seg["start"])
            end = float(seg["end"])
            duration = end - start
            speaker = seg["speaker"]
            fh.write(
                f"SPEAKER {recording_id} {channel} {start:.3f} {duration:.3f} "
                f"<NA> <NA> {speaker} <NA> <NA>\n"
            )


# ---------------------------------------------------------------------------
# Convert to pyannote Annotation
# ---------------------------------------------------------------------------


def segments_to_annotation(
    segments: list[dict[str, Any]],
) -> Annotation:
    """Convert a list of segment dicts to a pyannote.core.Annotation.

    Segments must have: start (float), end (float), speaker (str).
    """
    annotation = Annotation()
    for seg in segments:
        start = float(seg["start"])
        end = float(seg.get("end", seg["start"] + seg.get("duration", 0.0)))
        speaker = seg["speaker"]
        annotation[Segment(start, end)] = speaker
    return annotation


# ---------------------------------------------------------------------------
# Convert from pyannote Annotation
# ---------------------------------------------------------------------------


def annotation_to_segments(
    annotation: Annotation,
    recording_id: str,
) -> list[dict[str, Any]]:
    """Convert a pyannote.core.Annotation to a list of segment dicts."""
    segments: list[dict[str, Any]] = []
    for segment, _, speaker in annotation.itertracks(yield_label=True):
        segments.append(
            {
                "recording_id": recording_id,
                "channel": 1,
                "start": round(segment.start, 6),
                "end": round(segment.end, 6),
                "duration": round(segment.end - segment.start, 6),
                "speaker": speaker,
            }
        )
    return segments
