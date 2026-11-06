# Speaker Diarization Evaluation Platform

> Compare speaker diarization models head-to-head with transparent DER/JER scoring and a live leaderboard.

---

## What It Does

Upload a hypothesis RTTM file (your model's speaker predictions) and score it against a human-annotated reference. Results are saved and displayed on a sortable leaderboard with full error breakdowns.

**Key principles:**
- Same audio + same reference for every model
- Fixed scoring policy (collar, overlap, aggregation) chosen before evaluation
- Failed runs shown but excluded from rankings
- Full transparency: miss rate, false alarm, confusion rate per model

---

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, FastAPI |
| Evaluation | pyannote.metrics, pyannote.core |
| Database | SQLite (async via SQLAlchemy + aiosqlite) |
| Frontend | React 18 + Vite |
| Charts | Recharts |
| Testing | pytest |

---

## Quick Start

### Backend

```powershell
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/docs** for the interactive API.

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** for the leaderboard UI.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/models` | Register a model |
| `GET` | `/api/models` | List all models |
| `GET` | `/api/models/{id}` | Model detail + stats |
| `DELETE` | `/api/models/{id}` | Delete a model |
| `POST` | `/api/recordings` | Register a recording |
| `GET` | `/api/recordings` | List all recordings |
| `POST` | `/api/evaluations` | Submit hypothesis RTTM → score |
| `GET` | `/api/evaluations` | List all runs |
| `GET` | `/api/evaluations/{id}` | Run detail |
| `POST` | `/api/evaluations/{id}/retry` | Re-score a run |
| `GET` | `/api/leaderboard` | Aggregated rankings |

---

## RTTM Format

```
SPEAKER {recording_id} 1 {start:.3f} {duration:.3f} <NA> <NA> {speaker} <NA> <NA>
```

Example:
```
SPEAKER sample_001 1 0.500 2.300 <NA> <NA> speaker_A <NA> <NA>
SPEAKER sample_001 1 3.000 1.800 <NA> <NA> speaker_B <NA> <NA>
```

---

## Running Tests

```powershell
cd backend
pytest tests/ -v
```

---

## Scoring a Single Pair from CLI

```powershell
python scripts/run_experiment.py `
  --reference backend/data/sample_reference.rttm `
  --hypothesis backend/data/sample_hypothesis.rttm `
  --collar 0.25
```

---

## Project Structure

```
speaker-diarization-evaluation/
├── backend/
│   ├── app/
│   │   ├── main.py                  ← FastAPI app
│   │   ├── api/routes/              ← health, models, evaluations, leaderboard
│   │   ├── adapters/                ← model integrations (mock, pyannote, …)
│   │   ├── evaluation/              ← rttm.py, scorer.py, validation.py
│   │   ├── services/                ← evaluation_service.py
│   │   ├── schemas/                 ← Pydantic v2 models
│   │   └── db/                      ← SQLAlchemy async + ORM
│   ├── tests/                       ← pytest suite
│   ├── data/                        ← sample RTTM files
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/                   ← Dashboard, Leaderboard, EvaluatePage, ModelDetail
│       ├── components/              ← NavBar, MetricCard, StatusBadge
│       └── services/api.js          ← Axios client
├── docs/
│   ├── methodology.md               ← Full methodology document
│   ├── scoring_policy.md            ← One-page scoring policy
│   └── model_registry.md           ← 10 model table
├── scripts/
│   ├── run_experiment.py            ← CLI scorer
│   └── bulk_score.py                ← Batch CSV scorer
└── experiments/                     ← Exploratory analysis
```

---

## Scoring Policy Summary

| Setting | Value |
|---------|-------|
| Collar | 0.25 s |
| Overlapping speech | Scored |
| Speaker count hint | Not given |
| DER aggregation | Duration-weighted |
| Scoring library | pyannote.metrics 3.2.x |
