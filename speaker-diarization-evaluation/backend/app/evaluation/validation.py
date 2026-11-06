from __future__ import annotations

"""Validation helpers for RTTM files and segment lists."""

from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# File-level validation
# ---------------------------------------------------------------------------


def validate_rttm_file(filepath: str | Path) -> tuple[bool, list[str]]:
    """Validate an RTTM file at the given path.

    Returns:
        (is_valid, list_of_error_strings)
    """
    filepath = Path(filepath)
    errors: list[str] = []

    if not filepath.exists():
        return False, [f"File not found: {filepath}"]

    if not filepath.is_file():
        return False, [f"Path is not a file: {filepath}"]

    if filepath.stat().st_size == 0:
        return False, ["File is empty."]

    try:
        with filepath.open("r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except OSError as exc:
        return False, [f"Cannot read file: {exc}"]

    has_speaker_line = False
    for lineno, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if parts[0].upper() != "SPEAKER":
            continue

        has_speaker_line = True

        if len(parts) < 10:
            errors.append(
                f"Line {lineno}: expected 10 fields, got {len(parts)}."
            )
            continue

        # start time
        try:
            start = float(parts[3])
        except ValueError:
            errors.append(f"Line {lineno}: start time '{parts[3]}' is not a number.")
            continue

        # duration
        try:
            duration = float(parts[4])
        except ValueError:
            errors.append(f"Line {lineno}: duration '{parts[4]}' is not a number.")
            continue

        if start < 0:
            errors.append(f"Line {lineno}: start time {start} is negative.")
        if duration <= 0:
            errors.append(f"Line {lineno}: duration {duration} must be positive.")

        speaker = parts[7]
        if not speaker or speaker == "<NA>":
            errors.append(f"Line {lineno}: speaker label is empty or '<NA>'.")

    if not has_speaker_line:
        errors.append("File contains no SPEAKER lines.")

    return len(errors) == 0, errors


# ---------------------------------------------------------------------------
# Segment-level validation
# ---------------------------------------------------------------------------


def validate_segments(
    segments: list[dict[str, Any]],
    audio_duration: float | None = None,
) -> tuple[bool, list[str]]:
    """Validate a list of segment dicts.

    Each segment must have: start (float), end (float), speaker (str).

    Args:
        segments: List of segment dicts.
        audio_duration: Optional total audio duration. When provided, segments
            must not extend beyond this value.

    Returns:
        (is_valid, list_of_error_strings)
    """
    errors: list[str] = []

    if not segments:
        errors.append("Segment list is empty.")
        return False, errors

    for idx, seg in enumerate(segments):
        label = f"Segment {idx}"

        # Required keys
        for key in ("start", "speaker"):
            if key not in seg:
                errors.append(f"{label}: missing key '{key}'.")

        start = seg.get("start")
        end = seg.get("end")
        duration = seg.get("duration")
        speaker = seg.get("speaker", "")

        # Resolve end
        if end is None and duration is not None:
            try:
                end = float(start) + float(duration)
            except (TypeError, ValueError):
                end = None

        # Validate types
        try:
            start = float(start)
        except (TypeError, ValueError):
            errors.append(f"{label}: start '{start}' is not a number.")
            continue

        try:
            end = float(end)
        except (TypeError, ValueError):
            errors.append(f"{label}: end/duration missing or not a number.")
            continue

        if start < 0:
            errors.append(f"{label}: start time {start:.3f} is negative.")
        if end <= start:
            errors.append(
                f"{label}: end {end:.3f} must be greater than start {start:.3f}."
            )
        if not speaker or not str(speaker).strip():
            errors.append(f"{label}: speaker label is empty.")

        if audio_duration is not None and end > audio_duration:
            errors.append(
                f"{label}: segment end {end:.3f} exceeds audio duration {audio_duration:.3f}."
            )

    return len(errors) == 0, errors
