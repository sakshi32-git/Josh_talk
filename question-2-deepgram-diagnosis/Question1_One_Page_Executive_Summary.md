# Executive Summary: Voice of India Diarization Benchmark
## A 2-Minute Briefing for Leadership & Product Reviewers

---

### The Problem
AI speech systems look flawless in controlled demos, but collapse under real Indian operating conditions. In conversational Indian audio—marked by rapid turn-taking, overlapping speech (12–22% of conversation time), code-switching (Hinglish), noisy telephony, and diverse regional accents—commercial and open-source models show error rates ranging from 4% to over 44%. 

Existing benchmarks (NIST, AMI) test clean, Western, single-microphone audio with forgiving 250ms collars and ignored overlaps, misrepresenting real-world enterprise performance.

---

### The Solution: VoI-DiarBench
Josh Talks and AI4Bharat are launching **VoI-DiarBench**, an independent, public, and verifiable leaderboard evaluating speech diarization ("who spoke when") across real Indian acoustic conditions.

```
       [ 100 Hours Held-Out Indian Audio ]
   Telephony (8kHz) | Room Mics | Video Calls | Field
                         │
                         ▼
       [ 10 Evaluated Diarization Engines ]
   Open-Source (pyannote, NeMo) | Cloud APIs (Deepgram, Google, Azure, AWS)
                         │
                         ▼
        [ Rigorous, Standardized Scoring ]
      DER (0.25s & 0.0s Collar) | JER | Scored Overlap
                         │
                         ▼
       [ Public Leaderboard with Confidence ]
     Bootstrap Significance (p < 0.01) | Sub-filters
```

---

### 3 Core Architectural Choices That Matter Most

1. **Overlapping Speech is 100% Scored (No "Cheat Collars"):**
   Traditional benchmarks ignore audio segments where two people speak simultaneously. Because Indian conversations frequently involve cross-talk and affirmative interjections ("haan", "theek hai"), our benchmark penalizes models that fail to isolate simultaneous speakers.

2. **Decoupled Acoustic Ground Truth (Double-Blind Multi-Mic Rig):**
   Ground-truth references are captured using individual, isolated lapel microphones for each participant simultaneously recorded alongside a shared boundary microphone. Annotations undergo double-blind human verification (Cohen’s $\kappa \ge 0.94$), ensuring ground truth is mathematically grounded in acoustic energy rather than subjective human listening.

3. **Multi-Faceted Leaderboard with Statistical Significance:**
   Rather than a single deceptive ranking, the leaderboard segments performance across **Linguistic Cluster** (North, South, East, West), **Acoustic Channel** (Telephony 8kHz vs. Room Mics), and **Speaker Count** (2 vs. 3–4 vs. 5+). A system is only promoted in rank if its performance delta achieves statistical significance ($p < 0.01$ via 10,000 paired bootstrap iterations).

---

### The Evaluated Field (10 Flagship Systems)
- **Open-Source Champions:** pyannote.audio 3.1, NVIDIA NeMo Sortformer v2.0, WhisperX hybrid.
- **Enterprise Hyperscalers:** Google Cloud Speech v2 (Chirp 2), AWS Transcribe, Microsoft Azure Speech.
- **Specialized Speech AI APIs:** Deepgram Nova-3, AssemblyAI Universal-2, Speechmatics Flow, ElevenLabs Scribe v2.

---

### Key Takeaway for Product & Engineering Teams
> **A single accuracy score is an illusion.** A model achieving a stellar 8% DER on a 2-person executive interview can catastrophic fail at 55% DER on a 4-person bilingual customer support call. VoI-DiarBench gives engineering teams the verified, transparent data needed to choose the exact model suited for their deployment constraints, budget, and latency targets.
