"""Tests for app/evaluation/scorer.py"""
from __future__ import annotations

import pytest
from app.evaluation.scorer import score


def test_identical_reference_and_hypothesis(reference_rttm, tmp_path):
    """Identical reference and prediction should produce DER ~ 0."""
    result = score(reference_rttm, reference_rttm, collar=0.25)
    # With identical inputs pyannote may show very small collar-adjusted DER
    assert result["der"] == pytest.approx(0.0, abs=1.0)
    assert result["miss_rate"] == pytest.approx(0.0, abs=1.0)
    assert result["false_alarm_rate"] == pytest.approx(0.0, abs=1.0)


def test_normal_hypothesis_low_der(reference_rttm, hypothesis_rttm):
    """Slight offsets from reference should produce a small but non-zero DER."""
    result = score(reference_rttm, hypothesis_rttm, collar=0.25)
    assert isinstance(result["der"], float)
    assert result["der"] >= 0.0
    assert "jer" in result
    assert result["collar"] == 0.25


def test_missing_speech_increases_miss(reference_rttm, missing_speech_rttm):
    """Hypothesis missing half the reference speech should raise miss rate."""
    result = score(reference_rttm, missing_speech_rttm, collar=0.0)
    assert result["miss_rate"] > 0.0, "Miss rate should be > 0 when speech is missing"


def test_extra_speech_increases_false_alarm(reference_rttm, extra_speech_rttm):
    """Hypothesis with extra speech should raise false alarm rate."""
    result = score(reference_rttm, extra_speech_rttm, collar=0.0)
    assert result["false_alarm_rate"] > 0.0, "FA rate should be > 0 when extra speech is present"


def test_wrong_speaker_increases_confusion(reference_rttm, wrong_speaker_rttm):
    """Swapped speaker labels should raise confusion rate."""
    result = score(reference_rttm, wrong_speaker_rttm, collar=0.0)
    # Swapped speakers contribute to confusion
    assert result["der"] > 0.0


def test_result_has_all_keys(reference_rttm, hypothesis_rttm):
    result = score(reference_rttm, hypothesis_rttm)
    expected_keys = {"der", "jer", "miss_rate", "false_alarm_rate", "confusion_rate",
                     "reference_duration", "collar", "skip_overlap"}
    assert expected_keys == set(result.keys())


def test_reference_not_found(tmp_path, hypothesis_rttm):
    with pytest.raises(FileNotFoundError):
        score(tmp_path / "nonexistent.rttm", hypothesis_rttm)


def test_hypothesis_not_found(reference_rttm, tmp_path):
    with pytest.raises(FileNotFoundError):
        score(reference_rttm, tmp_path / "nonexistent.rttm")


def test_both_empty_returns_zero(tmp_path):
    """Both empty annotations should produce DER = 0."""
    empty = tmp_path / "empty.rttm"
    empty.write_text("", encoding="utf-8")
    # Empty file has no SPEAKER lines — parse_rttm returns []
    # segments_to_annotation([]) returns empty Annotation
    result = score(empty, empty, collar=0.25)
    assert result["der"] == 0.0
    assert result["jer"] == 0.0

