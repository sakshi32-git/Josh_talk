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


python analyze_sessions.py           # Re-computes correlations and saves PNG charts
```
