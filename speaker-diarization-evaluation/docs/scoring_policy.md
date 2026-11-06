# Scoring Policy

**Version:** 1.0  
**Date:** 2026-11-04  
**Status:** Fixed (locked before any model evaluation)

---

## Core Parameters

| Parameter | Value |
|-----------|-------|
| Collar | **0.25 seconds** |
| Score overlapping speech | **Yes** |
| Speaker count given to models | **No** |
| Audio format | 16 kHz, mono WAV, peak-normalized |
| DER aggregation | **Duration-weighted** average across recordings |
| Speaker mapping algorithm | Optimal assignment (Hungarian / pyannote.metrics) |
| Scoring library | `pyannote.metrics 3.2.x` |

---

## Failed Run Policy

- A run is **failed** if the model throws an exception, times out (> 300 s), or produces invalid/empty RTTM output.
- Failed runs are **excluded from DER/JER rankings**.
- Failed runs are **shown** in the "Coverage & Failures" section of the leaderboard.
- Treating a failed run as DER = 0 is **explicitly prohibited**.

---

## Aggregate DER Computation

$$\text{Aggregate DER} = \frac{\sum_i (\text{Miss}_i + \text{FA}_i + \text{Confusion}_i)}{\sum_i \text{Reference Duration}_i}$$

This is duration-weighted, so longer recordings have proportionally more influence on the final score.

---

## Collar

A collar of **0.25 s** is applied symmetrically around each segment boundary. Scoring errors within this collar window are not penalized. This is the standard value in the DIHARD and CHiME-6 challenges.

---

## Overlap Handling

Overlapping speech regions are **included** in scoring. This reflects real-world diarization difficulty and penalizes models that cannot handle simultaneous speakers.

To score with overlap excluded, use the `skip_overlap=True` parameter in the API (reported separately, not used for primary ranking).

---

## Reproducibility

All runs record:
- Model name, provider, and version
- Exact API parameters or local config
- Recording ID and audio hash (SHA-256)
- Collar and overlap settings
- Timestamp and runtime
- Raw output + normalized RTTM

