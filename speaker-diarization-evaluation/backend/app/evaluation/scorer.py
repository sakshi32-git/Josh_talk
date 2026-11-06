from __future__ import annotations

"""Scoring module using pyannote.metrics.

Computes DER, JER, miss rate, false alarm rate, and confusion rate between
a reference RTTM and a hypothesis RTTM.
"""

from pathlib import Path
from typing import Any

from pyannote.core import Annotation
from pyannote.metrics.diarization import DiarizationErrorRate, JaccardErrorRate

from app.evaluation.rttm import parse_rttm, segments_to_annotation


def score(
    reference_rttm_path: str | Path,
    hypothesis_rttm_path: str | Path,
    collar: float = 0.25,
    skip_overlap: bool = False,
) -> dict[str, Any]:
    """Score a hypothesis RTTM against a reference RTTM.

    Args:
        reference_rttm_path: Path to the reference RTTM file.
        hypothesis_rttm_path: Path to the hypothesis RTTM file.
        collar: Collar duration in seconds around boundaries (default 0.25).
        skip_overlap: If True, overlapping regions are excluded from scoring.

    Returns:
        dict with keys:
            der, jer, miss_rate, false_alarm_rate, confusion_rate,
            reference_duration, collar, skip_overlap
    """
    reference_rttm_path = Path(reference_rttm_path)
    hypothesis_rttm_path = Path(hypothesis_rttm_path)

    # -----------------------------------------------------------------------
    # File existence checks
    # -----------------------------------------------------------------------
    if not reference_rttm_path.exists():
        raise FileNotFoundError(f"Reference RTTM not found: {reference_rttm_path}")
    if not hypothesis_rttm_path.exists():
        raise FileNotFoundError(f"Hypothesis RTTM not found: {hypothesis_rttm_path}")

    # -----------------------------------------------------------------------
    # Parse
    # -----------------------------------------------------------------------
    ref_segments = parse_rttm(reference_rttm_path)
    hyp_segments = parse_rttm(hypothesis_rttm_path)

    reference: Annotation = segments_to_annotation(ref_segments)
    hypothesis: Annotation = segments_to_annotation(hyp_segments)

    # -----------------------------------------------------------------------
    # Edge-case: both empty → perfect score
    # -----------------------------------------------------------------------
    ref_duration = reference.get_timeline().duration()

    if ref_duration == 0.0:
        hyp_duration = hypothesis.get_timeline().duration()
        if hyp_duration == 0.0:
            # Both empty → DER = 0
            return {
                "der": 0.0,
                "jer": 0.0,
                "miss_rate": 0.0,
                "false_alarm_rate": 0.0,
                "confusion_rate": 0.0,
                "reference_duration": 0.0,
                "collar": collar,
                "skip_overlap": skip_overlap,
            }
        else:
            # Reference empty but hypothesis has speech → all false alarm
            raise ValueError(
                "Reference annotation is empty while hypothesis contains speech. "
                "Cannot compute meaningful DER."
            )

    # -----------------------------------------------------------------------
    # DER
    # -----------------------------------------------------------------------
    der_metric = DiarizationErrorRate(collar=collar, skip_overlap=skip_overlap)
    der_detail = der_metric(reference, hypothesis, detailed=True)

    total_ref = der_detail.get("total", ref_duration) or ref_duration

    miss = der_detail.get("missed detection", 0.0)
    fa = der_detail.get("false alarm", 0.0)
    conf = der_detail.get("confusion", 0.0)

    miss_rate = miss / total_ref if total_ref > 0 else 0.0
    fa_rate = fa / total_ref if total_ref > 0 else 0.0
    conf_rate = conf / total_ref if total_ref > 0 else 0.0
    der_value = miss_rate + fa_rate + conf_rate

    # -----------------------------------------------------------------------
    # JER
    # -----------------------------------------------------------------------
    jer_metric = JaccardErrorRate(collar=collar, skip_overlap=skip_overlap)
    jer_value = jer_metric(reference, hypothesis)

    return {
        "der": round(float(der_value) * 100, 4),          # percentage
        "jer": round(float(jer_value) * 100, 4),           # percentage
        "miss_rate": round(float(miss_rate) * 100, 4),
        "false_alarm_rate": round(float(fa_rate) * 100, 4),
        "confusion_rate": round(float(conf_rate) * 100, 4),
        "reference_duration": round(float(total_ref), 4),
        "collar": collar,
        "skip_overlap": skip_overlap,
    }
