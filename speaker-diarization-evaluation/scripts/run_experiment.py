#!/usr/bin/env python3
"""Quick CLI to score one reference RTTM against one hypothesis RTTM.

Usage:
    python scripts/run_experiment.py \\
        --reference backend/data/sample_reference.rttm \\
        --hypothesis backend/data/sample_hypothesis.rttm \\
        --collar 0.25
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.evaluation.scorer import score


def main() -> None:
    parser = argparse.ArgumentParser(description="Score a diarization hypothesis against a reference.")
    parser.add_argument("--reference", required=True, help="Path to reference RTTM file")
    parser.add_argument("--hypothesis", required=True, help="Path to hypothesis RTTM file")
    parser.add_argument("--collar", type=float, default=0.25, help="Collar in seconds (default: 0.25)")
    parser.add_argument("--skip-overlap", action="store_true", help="Skip overlapping speech regions")
    args = parser.parse_args()

    print(f"\nReference : {args.reference}")
    print(f"Hypothesis: {args.hypothesis}")
    print(f"Collar    : {args.collar}s")
    print(f"Overlap   : {'skipped' if args.skip_overlap else 'scored'}\n")

    try:
        result = score(
            reference_rttm_path=args.reference,
            hypothesis_rttm_path=args.hypothesis,
            collar=args.collar,
            skip_overlap=args.skip_overlap,
        )
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    col_w = 25
    print(f"{'Metric':<{col_w}} {'Value':>10}")
    print("-" * (col_w + 12))
    for key, label in [
        ("der",              "DER (%)"),
        ("jer",              "JER (%)"),
        ("miss_rate",        "Miss Rate (%)"),
        ("false_alarm_rate", "False Alarm (%)"),
        ("confusion_rate",   "Confusion (%)"),
        ("reference_duration", "Ref Duration (s)"),
    ]:
        val = result[key]
        print(f"{label:<{col_w}} {val:>10.4f}")
    print()


if __name__ == "__main__":
    main()

