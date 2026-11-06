"""Tests for app/evaluation/rttm.py"""
from __future__ import annotations

from pathlib import Path
import pytest

from app.evaluation.rttm import parse_rttm, write_rttm, segments_to_annotation, annotation_to_segments


SAMPLE_RTTM = """\
SPEAKER rec_001 1 0.000 3.000 <NA> <NA> speaker_A <NA> <NA>
SPEAKER rec_001 1 3.500 2.500 <NA> <NA> speaker_B <NA> <NA>
SPEAKER rec_001 1 6.200 4.000 <NA> <NA> speaker_A <NA> <NA>
"""


def test_parse_rttm_valid(tmp_path: Path):
    f = tmp_path / "test.rttm"
    f.write_text(SAMPLE_RTTM, encoding="utf-8")

    segs = parse_rttm(f)
    assert len(segs) == 3
    assert segs[0]["recording_id"] == "rec_001"
    assert segs[0]["start"] == pytest.approx(0.0)
    assert segs[0]["end"] == pytest.approx(3.0)
    assert segs[0]["speaker"] == "speaker_A"
    assert segs[1]["speaker"] == "speaker_B"


def test_parse_rttm_ignores_comments(tmp_path: Path):
    content = "# This is a comment\n" + SAMPLE_RTTM
    f = tmp_path / "test.rttm"
    f.write_text(content, encoding="utf-8")
    segs = parse_rttm(f)
    assert len(segs) == 3


def test_parse_rttm_ignores_blank_lines(tmp_path: Path):
    content = "\n" + SAMPLE_RTTM + "\n\n"
    f = tmp_path / "test.rttm"
    f.write_text(content, encoding="utf-8")
    segs = parse_rttm(f)
    assert len(segs) == 3


def test_parse_rttm_missing_fields(tmp_path: Path):
    f = tmp_path / "bad.rttm"
    f.write_text("SPEAKER rec 1 0.0 1.0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="fields"):
        parse_rttm(f)


def test_write_and_reread_rttm(tmp_path: Path):
    segs = [
        {"recording_id": "r1", "start": 0.5, "end": 2.3, "speaker": "A"},
        {"recording_id": "r1", "start": 2.5, "end": 4.0, "speaker": "B"},
    ]
    out = tmp_path / "out.rttm"
    write_rttm(segs, out)
    assert out.exists()

    parsed = parse_rttm(out)
    assert len(parsed) == 2
    assert parsed[0]["speaker"] == "A"
    assert parsed[0]["start"] == pytest.approx(0.5)
    assert parsed[0]["end"] == pytest.approx(2.3, rel=1e-3)
    assert parsed[1]["speaker"] == "B"


def test_segments_to_annotation(tmp_path: Path):
    f = tmp_path / "test.rttm"
    f.write_text(SAMPLE_RTTM, encoding="utf-8")
    segs = parse_rttm(f)
    ann = segments_to_annotation(segs)
    labels = set(ann.labels())
    assert "speaker_A" in labels
    assert "speaker_B" in labels
    assert ann.get_timeline().duration() == pytest.approx(9.5, rel=0.01)


def test_annotation_to_segments_roundtrip(tmp_path: Path):
    f = tmp_path / "test.rttm"
    f.write_text(SAMPLE_RTTM, encoding="utf-8")
    segs = parse_rttm(f)
    ann = segments_to_annotation(segs)
    back = annotation_to_segments(ann, "rec_001")
    assert len(back) == len(segs)
    for s in back:
        assert s["recording_id"] == "rec_001"
        assert s["end"] > s["start"]

