# Speaker Diarization Evaluation Platform

## End-to-End Implementation Guide

**Goal:** Build a platform that runs different speaker diarization
systems on the same audio, compares their predictions with
human-annotated reference files, calculates DER/JER, and displays
transparent results in a leaderboard.

> Josh Talks Question 1 is primarily a research and design task. The
> platform is a useful prototype. The assignment's key deliverables are
> the main methodology document, one-page report, leaderboard sketch,
> and a 2--3 minute video. A small experiment with 2--3 public
> recordings and 2--3 systems is optional.

------------------------------------------------------------------------

## 1. How the platform works

``` text
Audio recordings + metadata
          |
          v
Human reference annotations (RTTM)
          |
          v
Run each diarization model on the same audio
          |
          v
Convert model outputs into common RTTM format
          |
          v
Compare predictions with human reference
          |
          v
Calculate DER, JER, Miss, False Alarm, Confusion
          |
          v
Save results and generate leaderboard
```

**Fairness rules** - Same audio and reference for every model. - Same
scoring settings for every model. - Record exact model name, version and
configuration. - Never manually correct model predictions. - Mark failed
runs as `failed`; never treat them as zero DER. - Show error breakdowns
and test coverage, not just one score.

## 2. Technology stack

  Component          Technology
  ------------------ ------------------------------------
  Backend            Python, FastAPI
  Evaluation         pyannote.metrics / dscore
  Audio processing   soundfile, librosa
  Data analysis      Pandas, NumPy
  Database           SQLite initially, PostgreSQL later
  Frontend           React + Vite
  Charts             Recharts
  Testing            pytest

## 3. Project structure

``` text
speaker-diarization-evaluation/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/routes/
│   │   ├── adapters/       # Model integrations
│   │   ├── evaluation/     # RTTM, DER, JER, validation
│   │   ├── services/
│   │   ├── schemas/
│   │   └── db/
│   ├── tests/
│   ├── data/
│   │   ├── audio/
│   │   ├── reference/
│   │   └── predictions/
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       └── services/
├── docs/
│   ├── methodology.md
│   ├── model_registry.md
│   └── scoring_policy.md
├── experiments/
├── scripts/
├── .gitignore
└── README.md
```

## 4. Setup the project

Install Python 3.10/3.11, Node.js LTS, Git and VS Code.

Windows PowerShell:

``` powershell
mkdir speaker-diarization-evaluation
cd speaker-diarization-evaluation
mkdir backend, frontend, docs, experiments, scripts
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Create `requirements.txt`:

``` text
fastapi
uvicorn[standard]
python-multipart
pyannote.core
pyannote.metrics
pandas
numpy
soundfile
pytest
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

After confirming everything works, save exact dependency versions:

``` bash
pip freeze > requirements-lock.txt
```

## 5. Prepare the data

For every recording, store: - Recording ID and audio file - Duration,
sample rate and channel count - Dataset/split and relevant condition
metadata - Human reference RTTM path

RTTM is the common format for timed speaker segments. Example:

``` text
SPEAKER recording_001 1 0.50 2.30 <NA> <NA> speaker_1 <NA> <NA>
```

The fields include recording ID, channel, start time, duration and
speaker ID.

Every model adapter should convert its output into a common structure:

``` json
{
  "recording_id": "recording_001",
  "segments": [
    {"start": 0.5, "end": 2.8, "speaker": "speaker_1"},
    {"start": 2.9, "end": 4.1, "speaker": "speaker_2"}
  ]
}
```

Then convert it to RTTM for scoring. Validate timestamps, speaker
labels, empty outputs and segments beyond audio duration.

Keep human references separate from model predictions. Do not expose
held-out reference files to model providers.

## 6. Build the evaluation engine

Start with **one recording and one prediction**. Do not integrate ten
models yet.

Create these modules:

``` text
evaluation/
├── rttm.py       # Read and write RTTM
├── validation.py # Check segments and files
└── scorer.py     # Calculate DER and JER
```

DER:

``` text
DER = (Missed Speech + False Alarm + Speaker Confusion)
      / Reference Speaker Time
```

-   **Miss:** Reference speech not detected by the model.
-   **False Alarm:** Speech detected where the reference has no speech.
-   **Confusion:** Speech assigned to the wrong speaker.
-   **JER:** A complementary speaker-wise error metric.

Use `pyannote.metrics` or `dscore` rather than implementing the scoring
mathematics from scratch. Verify the installed package API and test it
with known examples.

**Required tests** 1. Identical reference and prediction should produce
zero DER/JER. 2. Different speaker names but identical speaker turns
should still score correctly after speaker mapping. 3. Missing speech
should increase Miss. 4. Extra speech should increase False Alarm. 5.
Wrong speaker assignment should increase Confusion. 6. Test overlapping
speech and collar settings.

## 7. Add model integrations

Create a common adapter interface:

``` python
class DiarizationAdapter:
    def diarize(self, audio_path):
        # Return segments with start, end and speaker
        raise NotImplementedError
```

Add models one by one. Research candidates such as: - pyannote.audio -
NVIDIA NeMo - SpeechBrain - Kaldi/VBx - Commercial APIs that provide
speaker labels

For Josh Talks, list at least **10 specific models/services** with
company, exact model name, type, and run method. Verify exact versions
and current availability before including them in the final report.

Save for every run: - Model/provider and exact version - API or
inference settings - Audio/recording ID - Runtime and request ID, if
available - Raw output and normalized RTTM - Status: completed, failed,
timed out or invalid output

## 8. Design the benchmark and scoring policy

Build a fixed test set that represents the intended use. Consider: -
2--8 speakers and different conversation types - Clean and noisy audio -
Overlapping speech and short turns - Different microphones and
environments - Relevant languages and accents, including Indian English
if that is a target use case

Use separate development and held-out test sets. Human reference
annotations should be reviewed by a second annotator, with disagreements
resolved and documented.

Decide and publish: - Boundary collar (tolerance around segment
boundaries) - Whether overlapping speech is scored - Whether the model
is told the number of speakers - Audio preprocessing and channel
policy - Treatment of vocalizations and uncertain segments

Apply one fixed scoring policy to all systems. Choose it before
reviewing model results.

## 9. Store results and create APIs

Use SQLite for the prototype; PostgreSQL can come later.

Core database entities: - `datasets` - `recordings` - `models` -
`evaluation_runs` - `scores`

Useful API endpoints:

  Endpoint                         Purpose
  -------------------------------- -----------------------
  `GET /api/health`                Check backend
  `POST /api/models`               Register model
  `POST /api/evaluations`          Start evaluation
  `GET /api/evaluations/{id}`      Get run result/status
  `GET /api/leaderboard`           Get rankings
  `GET /api/models/{id}/results`   Model-level breakdown

For longer model/API calls, use background jobs. Failed runs must be
excluded from rankings but shown in coverage/failure information.

## 10. Build the leaderboard frontend

Create these pages: - **Dashboard:** Number of models, recordings and
completed/failed runs. - **Leaderboard:** Rank, model/version, DER, JER,
Miss, False Alarm, Confusion, coverage and runtime. - **Model details:**
Performance by recording condition, error breakdown and model
configuration.

Add filters for dataset, language/accent, speaker count, noise, overlap
and model type.

Do not rank systems only by one headline score. A model may perform well
on clean audio but poorly on noisy or overlapping speech.

## 11. Statistical comparison and quality checks

A small DER difference does not automatically prove one model is better.

-   Score models on the same recordings.
-   Compare paired per-recording results.
-   Use bootstrap confidence intervals where appropriate.
-   Report the number of successful recordings and failures.
-   State whether aggregate DER is duration-weighted or an average of
    recording-level DER.

Test invalid RTTM, empty outputs, API timeouts, rate limits, corrupt
audio and model failures. Keep regression tests for known examples.

## 12. Development roadmap

  -----------------------------------------------------------------------
  Step                    Build                   Completion condition
  ----------------------- ----------------------- -----------------------
  1                       Setup and folder        Backend starts
                          structure               

  2                       RTTM parser and         Valid/invalid files
                          validator               tested

  3                       DER/JER scorer          Controlled tests pass

  4                       One model adapter       Model returns standard
                                                  segments

  5                       Full evaluation cycle   Audio → model → score
                                                  works

  6                       Database and APIs       Results are saved and
                                                  retrieved

  7                       More model adapters     10+ systems researched;
                                                  feasible integrations
                                                  added

  8                       Benchmark dataset       Fixed split and
                                                  reviewed references

  9                       Leaderboard UI          Rankings and filters
                                                  work

  10                      Statistics and          Results are
                          documentation           reproducible
  -----------------------------------------------------------------------

**Recommended order:** Finish steps 1--5 before building the complete
leaderboard.

## 13. Run the existing MVP

The starter MVP already has a FastAPI backend, RTTM upload, DER/JER
scoring, SQLite storage and a basic leaderboard.

``` bash
cd backend
python -m venv .venv
```

Windows:

``` powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

macOS/Linux:

``` bash
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

Upload `sample_reference.rttm` as the reference and
`sample_hypothesis.rttm` as the prediction. These are toy files for
testing the software only---not real benchmark results.

Before proceeding, confirm that the dashboard opens, scoring works,
results are saved, and the leaderboard updates.

## 14. Final Josh Talks Question 1 checklist

**Main document** - \[ \] Purpose and intended users - \[ \] At least 10
named models/services - \[ \] Company, exact model, type and run
method - \[ \] Fair comparison rules - \[ \] Test data design and
human-reference quality checks - \[ \] Primary/supporting metrics and
definitions - \[ \] Collar, overlap and speaker-count policy - \[ \]
Audio-to-leaderboard evaluation process - \[ \] Statistical comparison
method - \[ \] Information shown beside every score - \[ \] Final
reflection answers

**Other deliverables** - \[ \] One-page report - \[ \] Leaderboard
sketch/mockup - \[ \] 2--3 minute video walkthrough

**Optional strong addition** - \[ \] Run 2--3 systems on 2--3 public
recordings - \[ \] Score with dscore or pyannote.metrics - \[ \] Record
exact model versions/settings and report findings

------------------------------------------------------------------------

**Final principle:** Every system must be evaluated against the same
human reference, on the same recordings, under the same published
scoring policy. The leaderboard should explain both model performance
and its limitations.
