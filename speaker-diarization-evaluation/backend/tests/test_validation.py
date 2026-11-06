"""Tests for app/evaluation/validation.py"""
from __future__ import annotations

from pathlib import Path
import pytest
from app.evaluation.validation import validate_rttm_file, validate_segments


# ---------------------------------------------------------------------------
# File validation
# ---------------------------------------------------------------------------

VALID_RTTM = """\
SPEAKER rec_001 1 0.000 3.000 <NA> <NA> speaker_A <NA> <NA>
SPEAKER rec_001 1 3.500 2.500 <NA> <NA> speaker_B <NA> <NA>
"""


def test_valid_rttm_file(tmp_path):
    f = tmp_path / "valid.rttm"
    f.write_text(VALID_RTTM, encoding="utf-8")
    is_valid, errors = validate_rttm_file(f)
    assert is_valid, f"Expected valid, got errors: {errors}"
    assert errors == []


def test_missing_file(tmp_path):
    is_valid, errors = validate_rttm_file(tmp_path / "missing.rttm")
    assert not is_valid
    assert any("not found" in e.lower() for e in errors)


def test_empty_file(tmp_path):
    f = tmp_path / "empty.rttm"
    f.write_text("", encoding="utf-8")
    is_valid, errors = validate_rttm_file(f)
    assert not is_valid


def test_negative_start_time(tmp_path):
    f = tmp_path / "neg.rttm"
    f.write_text("SPEAKER rec 1 -1.0 2.0 <NA> <NA> spk_A <NA> <NA>\n", encoding="utf-8")
    is_valid, errors = validate_rttm_file(f)
    assert not is_valid
    assert any("negative" in e.lower() for e in errors)


def test_zero_duration(tmp_path):
    f = tmp_path / "zero_dur.rttm"
    f.write_text("SPEAKER rec 1 0.0 0.0 <NA> <NA> spk_A <NA> <NA>\n", encoding="utf-8")
    is_valid, errors = validate_rttm_file(f)
    assert not is_valid


# ---------------------------------------------------------------------------
# Segment validation
# ---------------------------------------------------------------------------

def test_valid_segments():
    segs = [
        {"start": 0.0, "end": 2.0, "speaker": "A"},
        {"start": 2.5, "end": 4.0, "speaker": "B"},
    ]
    is_valid, errors = validate_segments(segs)
    assert is_valid, errors


def test_empty_segment_list():
    is_valid, errors = validate_segments([])
    assert not is_valid


def test_negative_start():
    segs = [{"start": -1.0, "end": 2.0, "speaker": "A"}]
    is_valid, errors = validate_segments(segs)
    assert not is_valid
    assert any("negative" in e.lower() for e in errors)


def test_end_before_start():
    segs = [{"start": 3.0, "end": 1.0, "speaker": "A"}]
    is_valid, errors = validate_segments(segs)
    assert not is_valid
    assert any("greater than start" in e.lower() for e in errors)


def test_empty_speaker():
    segs = [{"start": 0.0, "end": 2.0, "speaker": ""}]
    is_valid, errors = validate_segments(segs)
    assert not is_valid
    assert any("speaker" in e.lower() for e in errors)


def test_segment_beyond_audio_duration():
    segs = [{"start": 5.0, "end": 15.0, "speaker": "A"}]
    is_valid, errors = validate_segments(segs, audio_duration=10.0)
    assert not is_valid
    assert any("exceeds" in e.lower() for e in errors)


def test_segment_within_audio_duration():
    segs = [{"start": 0.0, "end": 5.0, "speaker": "A"}]
    is_valid, errors = validate_segments(segs, audio_duration=10.0)
    assert is_valid

