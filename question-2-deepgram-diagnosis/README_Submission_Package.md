# Josh Talks Growth Assessment: Master Submission Package
## Candidate Submission & Project Guide
**Initiative:** Voice of India Diarization Benchmark & Deepgram Nova-3 Root Cause Analysis  
**Organization:** Josh Talks & AI4Bharat (IIT Madras)

---

## 📁 Repository & Submission Index

This folder contains the complete, production-grade solutions for both **Question 1** and **Question 2**, including technical specifications, code, charts, social copy, and video scripts.

```
joshtalk_assign/
│
├── Joshtalks_Growth_Assessment (1).pdf              # Original Assignment Specification
│
├── [ QUESTION 1: LEADERBOARD SYSTEM DESIGN ]
│   ├── Question1_Diarization_Leaderboard_Design.md  # Deliverable 1: Comprehensive Main Design Document + Reflection
│   ├── Question1_One_Page_Executive_Summary.md      # Deliverable 2: 2-Minute High-Impact Summary for Leadership
│   ├── Question1_Leaderboard_UI_Specification_and_Wireframe.md # Deliverable 3: Leaderboard UI Wireframe & Product Specs
│   └── Question1_Video_Walkthrough_Script.md        # Deliverable 4: 2.5-Minute Video Recording Script
│
├── [ QUESTION 2: DEEPGRAM NOVA-3 ROOT CAUSE DIAGNOSIS ]
│   ├── Sakshi_Sonker_Report.md                      # Deliverable 1: Part A (Diagnostics) + Part B (Research Report)
│   ├── Sakshi_Sonker_Posts.md                       # Deliverable 2: Part C Social Media Copy (X Thread & LinkedIn)
│   ├── Sakshi_Sonker_Proof.md                       # Deliverable 3: Deepgram Playground Verification Matrix & Audit Log
│   ├── analyze_sessions.py                          # Deliverable 4: Working Python Code for Statistical Correlations
│   ├── deepgram_error_decomposition_chart.png       # Generated Visual: Error Decomposition (MS vs FA vs SC)
│   ├── deepgram_overlap_vs_der_chart.png            # Generated Visual: Overlap % vs DER Correlation Chart
│   └── Question2_Video_Walkthrough_Script.md        # Deliverable 5: 2.5-Minute Video Walkthrough Script
│
└── README_Submission_Package.md                     # This Master Guide
```

---

## 🚀 Key Results & Highlights

### 1. Question 1: System Design Overview
- **Evaluated Fleet:** 10 diverse systems (pyannote.audio 3.1, NVIDIA NeMo Sortformer, Deepgram Nova-3, AssemblyAI Universal-2, Google Chirp 2, Azure AI Speech, ElevenLabs Scribe v2, AWS Transcribe, WhisperX, Speechmatics Flow).
- **Acoustic Integrity:** 100-hour held-out Indian speech dataset collected via multi-channel synchronous capture (isolated lapels + room mic) with double-blind human verification ($\kappa \ge 0.94$).
- **Strict Scoring with Scored Overlap:** Full overlap scoring and dual reporting (0.25s standard collar + 0.0s strict collar) with 10,000 paired bootstrap iterations to verify statistical significance ($p < 0.01$).

### 2. Question 2: Deepgram Nova-3 Root Cause Diagnosis
- **The Finding:** Over **80% of Nova-3's 67.1% DER is driven by Missed Speech**, not speaker confusion.
- **Root Cause Confirmed:** In joint ASR-diarization models, speaker timestamps are strictly bound to recognized word tokens. When rapid interruptions, backchannels ("mm-hm", "haan"), or overlapping secondary voices are dropped by the ASR decoder, the corresponding time intervals vanish completely from the speaker timeline, generating massive missed speech penalties under strict 0.0s collar scoring.
- **Hypotheses Ruled Out:** Signal-to-noise ratio / background noise ($r = -0.007$), regional accent bias, digital clipping (0.0% clipped samples), and speaker clustering confusion.

---

## 🎥 Recording Your Walkthrough Videos (Quick Checklist)
1. **Question 1 Video (2–3 mins):** Use `Question1_Video_Walkthrough_Script.md`. Open `Question1_Leaderboard_UI_Specification_and_Wireframe.md` or slides on screen.
2. **Question 2 Video (2–3 mins):** Use `Question2_Video_Walkthrough_Script.md`. Display `deepgram_error_decomposition_chart.png` and `deepgram_overlap_vs_der_chart.png` on screen while speaking.

