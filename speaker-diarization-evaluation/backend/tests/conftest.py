"""Shared pytest fixtures for the backend test suite."""
from __future__ import annotations

from pathlib import Path
import pytest


REFERENCE_RTTM_CONTENT = """\
SPEAKER rec_001 1 0.000 3.000 <NA> <NA> speaker_A <NA> <NA>
SPEAKER rec_001 1 3.500 2.500 <NA> <NA> speaker_B <NA> <NA>
SPEAKER rec_001 1 6.200 4.000 <NA> <NA> speaker_A <NA> <NA>
SPEAKER rec_001 1 10.500 2.000 <NA> <NA> speaker_B <NA> <NA>
"""

# Hypothesis: slight offsets + same speaker turns = small DER
HYPOTHESIS_RTTM_CONTENT = """\
SPEAKER rec_001 1 0.100 2.800 <NA> <NA> spk_0 <NA> <NA>
SPEAKER rec_001 1 3.600 2.300 <NA> <NA> spk_1 <NA> <NA>
SPEAKER rec_001 1 6.300 3.800 <NA> <NA> spk_0 <NA> <NA>
SPEAKER rec_001 1 10.600 1.800 <NA> <NA> spk_1 <NA> <NA>
"""

# Hypothesis with missing speech (only 2 of 4 turns)
MISSING_SPEECH_RTTM = """\
SPEAKER rec_001 1 0.000 3.000 <NA> <NA> spk_0 <NA> <NA>
SPEAKER rec_001 1 3.500 2.500 <NA> <NA> spk_1 <NA> <NA>
"""

# Hypothesis with extra speech (adds extra segment)
EXTRA_SPEECH_RTTM = """\
SPEAKER rec_001 1 0.000 3.000 <NA> <NA> spk_0 <NA> <NA>
SPEAKER rec_001 1 3.500 2.500 <NA> <NA> spk_1 <NA> <NA>
SPEAKER rec_001 1 6.200 4.000 <NA> <NA> spk_0 <NA> <NA>
SPEAKER rec_001 1 10.500 2.000 <NA> <NA> spk_1 <NA> <NA>
SPEAKER rec_001 1 13.000 3.000 <NA> <NA> spk_0 <NA> <NA>
"""

# Hypothesis with inconsistent speaker assignment (merges speaker turns into one speaker, causing confusion)
WRONG_SPEAKER_RTTM = """\
SPEAKER rec_001 1 0.000 3.000 <NA> <NA> spk_0 <NA> <NA>
SPEAKER rec_001 1 3.500 2.500 <NA> <NA> spk_0 <NA> <NA>
SPEAKER rec_001 1 6.200 4.000 <NA> <NA> spk_0 <NA> <NA>
SPEAKER rec_001 1 10.500 2.000 <NA> <NA> spk_1 <NA> <NA>
"""


@pytest.fixture
def reference_rttm(tmp_path: Path) -> Path:
    p = tmp_path / "reference.rttm"
    p.write_text(REFERENCE_RTTM_CONTENT, encoding="utf-8")
    return p


@pytest.fixture
def hypothesis_rttm(tmp_path: Path) -> Path:
    p = tmp_path / "hypothesis.rttm"
    p.write_text(HYPOTHESIS_RTTM_CONTENT, encoding="utf-8")
    return p


@pytest.fixture
def missing_speech_rttm(tmp_path: Path) -> Path:
    p = tmp_path / "missing_speech.rttm"
    p.write_text(MISSING_SPEECH_RTTM, encoding="utf-8")
    return p


@pytest.fixture
def extra_speech_rttm(tmp_path: Path) -> Path:
    p = tmp_path / "extra_speech.rttm"
    p.write_text(EXTRA_SPEECH_RTTM, encoding="utf-8")
    return p


@pytest.fixture
def wrong_speaker_rttm(tmp_path: Path) -> Path:
    p = tmp_path / "wrong_speaker.rttm"
    p.write_text(WRONG_SPEAKER_RTTM, encoding="utf-8")
    return p

