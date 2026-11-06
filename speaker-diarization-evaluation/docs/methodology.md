# Methodology: Speaker Diarization Evaluation Platform

## 1. Purpose and Intended Users

This platform enables fair, reproducible comparison of speaker diarization systems. It is intended for:
- **ML engineers** evaluating diarization models for production use at Josh Talks
- **Researchers** benchmarking new approaches against established baselines
- **Decision-makers** needing transparent, comparable scores across vendors

---

## 2. The 10 Diarization Systems Under Evaluation

| # | Model Name | Provider | Type | Run Method |
|---|-----------|----------|------|-----------|
| 1 | `pyannote/speaker-diarization-3.1` | pyannote.audio (HuggingFace) | Open Source | Local Python pipeline |
| 2 | `NeMo MSDD (Multi-Scale Diarization Decoder)` | NVIDIA | Open Source | Local via `nemo_toolkit` |
| 3 | `SpeechBrain ECAPA-TDNN` | SpeechBrain | Open Source | Local via `speechbrain` package |
| 4 | `Amazon Transcribe` | Amazon Web Services | Commercial API | REST API (`boto3`) |
| 5 | `Google Speech-to-Text v2 (with diarization)` | Google Cloud | Commercial API | REST API (`google-cloud-speech`) |
| 6 | `Azure Cognitive Services Speaker Diarization` | Microsoft | Commercial API | REST API (`azure-cognitiveservices-speech`) |
| 7 | `AssemblyAI` | AssemblyAI | Commercial API | REST API (HTTP + polling) |
| 8 | `Rev.ai` | Rev.ai | Commercial API | REST API (`rev_ai` Python SDK) |
| 9 | `Kaldi/VBx` | Brno University of Technology | Open Source | Docker container / CLI |
| 10 | `Whisper + pyannote pipeline` | OpenAI + pyannote.audio | Open Source | Local (Whisper ASR → pyannote diarize) |

> **Note:** Exact model versions and API endpoints must be verified at integration time. Versions recorded in `model_registry.md`.

---

## 3. Fair Comparison Rules

1. **Same audio** — every model receives the identical audio file and identical preprocessing.
2. **Same reference** — every model is scored against the same human-annotated RTTM.
3. **Same scoring policy** — collar, overlap handling, speaker-count assumption are fixed before any model is run (see Section 7).
4. **Exact version tracking** — model name, version, and configuration are recorded per run.
5. **No manual correction** — model outputs are never edited before scoring.
6. **Failed runs are excluded from rankings** but shown in coverage statistics.
7. **Number of speakers is not given** to any model unless that model requires it by design (documented per model).

---

## 4. Metrics and Definitions

### Diarization Error Rate (DER)

$$\text{DER} = \frac{\text{Missed Speech} + \text{False Alarm} + \text{Speaker Confusion}}{\text{Reference Speaker Time}}$$

- **Missed Speech (Miss):** Reference speech that the model did not detect.
- **False Alarm (FA):** Speech detected where the reference contains no speech.
- **Speaker Confusion:** Speech correctly detected but attributed to the wrong speaker.

### Jaccard Error Rate (JER)

A complementary metric that averages per-speaker Jaccard distances; less sensitive to overall duration imbalances.

Both metrics are computed using `pyannote.metrics` (open-source, audited implementation).

---

## 5. Test Data Design

### Corpus construction principles
- 2–8 speakers per recording
- Multiple conversation types: interviews, panel discussions, phone calls, lectures
- Balanced across: **clean**, **noisy**, and **overlapping** conditions
- Multiple microphone types (close-talk, far-field)
- Languages: English, Indian English (a target use case for Josh Talks), and Hindi-English code-switching

### Dataset split
| Split | Purpose | Exposed to model providers? |
|-------|---------|---------------------------|
| Development | Hyperparameter tuning | Allowed |
| **Test (held out)** | Official benchmark ranking | **No** |

### Reference annotation quality
- Human annotators use ELAN or Audacity with RTTM export
- Each recording reviewed by a **second independent annotator**
- Disagreements discussed and resolved; resolution notes documented
- Inter-annotator agreement (IAA) measured and reported alongside scores

---

## 6. Scoring Policy

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Collar | 0.25 s | Standard tolerance for segment boundary imprecision |
| Overlapping speech | **Scored** | Reflects real-world performance on overlapping speech |
| Number of speakers given to model | **No** | Oracle speaker count gives unfair advantage |
| Audio preprocessing | 16 kHz mono WAV, peak-normalized | Consistent, model-agnostic format |
| Aggregate DER | **Duration-weighted** | Prevents short recordings from dominating |
| Speaker mapping | Optimal (Hungarian algorithm) | Via pyannote.metrics internals |

This policy is **fixed before viewing any model results** and applies equally to all systems.

---

## 7. Audio-to-Leaderboard Evaluation Process

```
1. Audio + Reference RTTM provided to platform
2. Each model/adapter called with the same audio
3. Adapter converts output → standard segment JSON
4. Segment JSON converted → hypothesis RTTM
5. Hypothesis RTTM validated (timestamps, labels, file format)
6. DER/JER computed: scorer.score(reference, hypothesis, collar=0.25)
7. Run saved to DB: model, version, settings, raw output, RTTM, metrics
8. Failed runs flagged; not ranked but shown in transparency table
9. Leaderboard aggregated per model, sorted by avg DER
```

---

## 8. Statistical Comparison Method

A small DER difference does not prove superiority.

- **Paired comparison:** Models are scored on the **same set of recordings**.
- **Bootstrap confidence intervals:** 10,000 bootstrap resamples of per-recording DER to estimate 95% CI.
- **Practical significance threshold:** Differences < 2% DER are treated as "comparable" unless CI is narrow.
- **Reporting:** Leaderboard shows: avg DER, 95% CI, number of recordings, number of failed runs.

---

## 9. Information Shown Beside Every Score

For every leaderboard entry:
- Model name, provider, version, model type, run method
- Average DER and JER (± 95% CI)
- Miss rate, False Alarm rate, Confusion rate
- Number of recordings evaluated / number failed
- Average runtime per recording
- Scoring collar and overlap policy used
- Link to run-level breakdown

---

## 10. Final Reflection

**Q: What makes a diarization leaderboard trustworthy?**
Transparency. Every decision — test data selection, annotation process, scoring parameters — must be documented and fixed before evaluation begins. The leaderboard should tell you not just *who won*, but *under what conditions* and *how reliably*.

**Q: Why is DER not enough?**
DER is duration-weighted and dominated by long segments. JER reveals per-speaker failures. Miss/FA/Confusion decomposition shows *why* a model fails. A model with low DER on clean audio may collapse on noisy or overlapping speech — the leaderboard must expose this.

**Q: How do you handle models that refuse to run?**
Failed and timed-out runs are logged with the error, excluded from DER rankings, and displayed in a separate "coverage failures" table. This prevents hiding unreliable models behind silence.

