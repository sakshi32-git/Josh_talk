#!/usr/bin/env python3
"""Bulk-score multiple (reference, hypothesis) RTTM pairs from a CSV file.

CSV format (header required):
    recording_id,reference_rttm,hypothesis_rttm

Usage:
    python scripts/bulk_score.py --input runs.csv --output results.csv --collar 0.25
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.evaluation.scorer import score


def main() -> None:
    parser = argparse.ArgumentParser(description="Bulk-score diarization predictions.")
    parser.add_argument("--input", required=True, help="CSV file with columns: recording_id,reference_rttm,hypothesis_rttm")
    parser.add_argument("--output", default="results.csv", help="Output CSV path (default: results.csv)")
    parser.add_argument("--collar", type=float, default=0.25)
    parser.add_argument("--skip-overlap", action="store_true")
    args = parser.parse_args()

    rows = []
    with open(args.input, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rec_id = row["recording_id"]
            ref = row["reference_rttm"]
            hyp = row["hypothesis_rttm"]
            print(f"Scoring {rec_id}…", end=" ", flush=True)
            try:
                result = score(ref, hyp, collar=args.collar, skip_overlap=args.skip_overlap)
                status = "completed"
                error = ""
            except Exception as e:
                result = {k: None for k in ["der","jer","miss_rate","false_alarm_rate","confusion_rate","reference_duration"]}
                status = "failed"
                error = str(e)
                print(f"FAILED: {e}")
            else:
                print(f"DER={result['der']:.2f}%")

            rows.append({
                "recording_id": rec_id,
                "reference_rttm": ref,
                "hypothesis_rttm": hyp,
                "status": status,
                "der": result["der"],
                "jer": result["jer"],
                "miss_rate": result["miss_rate"],
                "false_alarm_rate": result["false_alarm_rate"],
                "confusion_rate": result["confusion_rate"],
                "reference_duration": result["reference_duration"],
                "collar": args.collar,
                "skip_overlap": args.skip_overlap,
                "error": error,
            })

    fieldnames = ["recording_id","reference_rttm","hypothesis_rttm","status",
                  "der","jer","miss_rate","false_alarm_rate","confusion_rate",
                  "reference_duration","collar","skip_overlap","error"]
    with open(args.output, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nResults written to {args.output}")
    completed = sum(1 for r in rows if r["status"] == "completed")
    print(f"Completed: {completed}/{len(rows)}")


if __name__ == "__main__":
    main()

