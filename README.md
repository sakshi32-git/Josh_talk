# Josh_talk

# Josh Talks Growth Assessment — Complete Submission Package
**Candidate:** Sakshi Sonker  
**Platform:** Voice of India Diarization Benchmark  

This repository contains the complete, production-grade solutions for **both Question 1 and Question 2** of the **Joshtalks Growth Assessment: Voice of India**.

---

## 📁 Repository Structure & Deliverables Map

```
josh_talk_final/
├── README.md                            <-- Master Repository Documentation
├── SUBMISSION_OVERVIEW.md               <-- Master Submission Guide
├── implementation.md                    <-- Initial end-to-end implementation plan
│
├── speaker-diarization-evaluation/      <-- QUESTION 1: Leaderboard Design & Software Prototype
│   ├── docs/
│   │   ├── question_1_main_methodology.md  <-- Deliverable 1: Main Methodology (32 KB, rigorous research)
│   │   ├── one_page_report.md             <-- Deliverable 2: One-Page Executive Report (2-min read)
│   │   ├── leaderboard_sketch.md          <-- Deliverable 3: Leaderboard Product Wireframe & Spec
│   │   ├── video_walkthrough_script.md    <-- Deliverable 4: Timed Video Walkthrough Script (2:45)
│   │   ├── scoring_policy.md              <-- Published Scoring Policy
│   │   └── model_registry.md              <-- 10 Evaluated Diarization Models
│   ├── backend/                           <-- Working Prototype Backend (FastAPI, pyannote.metrics)
│   │   ├── app/                           <-- API routes, DB models, schemas, adapters, services
│   │   ├── tests/                         <-- Unit test suite (28/28 tests passing)
│   │   └── requirements.txt
│   ├── frontend/                          <-- Working Prototype Frontend (React 18 + Vite + Recharts)
│   └── scripts/                           <-- CLI experiment runners (run_experiment.py, bulk_score.py)
│
└── question-2-deepgram-diagnosis/       <-- QUESTION 2: Deepgram Nova-3 Failure Diagnosis
    ├── Sakshi_Sonker_Report.md               <-- Deliverable 1: Research Report (Parts A & B answered)
    ├── Sakshi_Sonker_Report.html             <-- Deliverable 1: Print-ready HTML (Ctrl+P -> PDF)
    ├── Sakshi_Sonker_Posts.md                <-- Deliverable 2: Social Media Posts (X Thread + LinkedIn)
    ├── Sakshi_Sonker_Proof.md                <-- Deliverable 3: Playground Proof & Verification Matrix
    ├── analyze_sessions.py                   <-- Deliverable 4: Analysis Script & Correlation Calculator
    ├── deepgram_error_decomposition_chart.png <-- Deliverable 4: Error decomposition chart (generated)
    ├── deepgram_overlap_vs_der_chart.png     <-- Deliverable 4: Overlap vs DER correlation chart (generated)
    └── Question2_Video_Walkthrough_Script.md <-- Deliverable 5: 2-3 minute Video Script for Question 2
```

---

## 🎯 Deliverables Checklist (Mapped to Assessment Instructions)

### Question 1: Design a Speaker Diarization Evaluation
| # | Assessment Deliverable | Location | Status |
|---|---|---|---|
| 1 | **Main Document** (Purpose, 10 models, fairness, test data, metrics, scoring, reflections) | `speaker-diarization-evaluation/docs/question_1_main_methodology.md` | ✅ Complete |
| 2 | **One-Page Report** (Core setup, key design bets, takeaway) | `speaker-diarization-evaluation/docs/one_page_report.md` | ✅ Complete |
| 3 | **Leaderboard Sketch** (Wireframe, filters, metric metadata) | `speaker-diarization-evaluation/docs/leaderboard_sketch.md` | ✅ Complete |
| 4 | **Video Walkthrough Script** (2–3 min presentation script) | `speaker-diarization-evaluation/docs/video_walkthrough_script.md` | ✅ Ready to record |
| + | **Working Platform Prototype** (FastAPI, React, pyannote.metrics, 28 passed tests) | `speaker-diarization-evaluation/` | ✅ Complete & Verified |

---

### Question 2: Diagnosing Deepgram Nova-3 Performance
| # | Assessment Deliverable | Target Filename | Location | Status |
|---|---|---|---|---|
| 1 | **The Report** (Part A questions answered + Part B research note) | `Sakshi_Sonker_Report.pdf` | `question-2-deepgram-diagnosis/Sakshi_Sonker_Report.md` | ✅ Complete (open `.html` and print to PDF) |
| 2 | **Social Media Posts** (Part C: 5-post X thread + 1,180-char LinkedIn post) | `Sakshi_Sonker_Posts` | `question-2-deepgram-diagnosis/Sakshi_Sonker_Posts.md` | ✅ Complete |
| 3 | **Playground Proof Audit** (Screenshots / proof protocol for 7 runs) | `Sakshi_Sonker_Proof` | `question-2-deepgram-diagnosis/Sakshi_Sonker_Proof.md` | ✅ Complete (capture screenshots) |
| 4 | **Working Code & Charts** (Correlation script + 2 PNG charts) | Code / Spreadsheet | `question-2-deepgram-diagnosis/analyze_sessions.py` | ✅ Complete & Tested |
| 5 | **Video Walkthrough Script** (2:45 min video script on root cause) | Video Link | `question-2-deepgram-diagnosis/Question2_Video_Walkthrough_Script.md` | ✅ Ready to record |

---

## 🚀 Quick Execution Guide

### 1. Run the Question 1 Prototype
```powershell
# Backend
cd speaker-diarization-evaluation\backend
python -m pytest tests/              # Runs all 28 test cases
uvicorn app.main:app --reload        # Starts API at http://127.0.0.1:8000/docs

# Frontend
cd ..\frontend
npm install
npm run dev                          # Starts UI at http://localhost:5173
```

### 2. Run the Question 2 Analysis & Chart Generator
```powershell
cd question-2-deepgram-diagnosis
python analyze_sessions.py           # Re-computes correlations and saves PNG charts
```
