# Leaderboard Product Specification & UI/UX Sketch
**Product:** Voice of India — Diarization-Bench Leaderboard  
**Target:** Web Portal & Interactive Decision Matrix  
**Status:** Product Design Document & Wireframe Specification  

---

## 1. Product Architecture & Page Layout

The Leaderboard is designed as an interactive decision intelligence portal for ML engineers, product managers, and enterprise buyers. It consists of four primary interface components:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  🎙️ VOICE OF INDIA   Leaderboard   Model Comparison   Submit Evaluation   Docs & Methodology   [API Docs]│
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  GLOBAL BENCHMARK FILTERS                                                                              │
│  Domain: [ All Domains ▼ ]  Collar: [ 0.25s (Standard) ▼ ]  Overlap: [ Scored (Strict) ▼ ]            │
│  Speaker Count: [ 2 to 8 ▼ ] Dialect/Accent: [ All India ▼ ] Sort By: [ Diarization Error Rate (DER) ▼] │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  AGGREGATE KPI BENCHMARK SUMMARY                                                                       │
│  ┌───────────────────────┐ ┌───────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐  │
│  │ EVALUATED SYSTEMS     │ │ TEST SET DURATION     │ │ SOTA BEST DER        │ │ MEDIAN COMMERCIAL DER│  │
│  │ 10 Models (4 OS / 6 C)│ │ 60.0 Hours (240 Files)│ │ 14.2% (pyannote 3.1) │ │ 19.4% (Google STT v2)│  │
│  └───────────────────────┘ └───────────────────────┘ └──────────────────────┘ └──────────────────────┘  │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  PRIMARY LEADERBOARD RANKINGS TABLE                                                                    │
│  [Search model name...]                             [Download CSV] [Download JSON] [Export BibTeX]     │
│  ┌────┬──────────────────────┬─────────┬──────────────┬──────────────┬──────────────┬─────────┬───────┐  │
│  │Rank│ Model / Provider     │ DER (%) │ Missed (%)   │ False Alm (%)│ Spk Conf (%) │ JER (%) │Status │  │
│  ├────┼──────────────────────┼─────────┼──────────────┼──────────────┼──────────────┼─────────┼───────┤  │
│  │ #1 │ pyannote 3.1         │ 14.2% ■ │ 4.8%         │ 2.1%         │ 7.3%         │ 21.4%   │ Passed│  │
│  │ #2 │ NVIDIA NeMo MSDD     │ 15.1% ■ │ 5.2%         │ 2.9%         │ 7.0%         │ 22.8%   │ Passed│  │
│  │ #3 │ Azure Conv-Trans     │ 17.8% ■ │ 7.1%         │ 1.8%         │ 8.9%         │ 25.1%   │ Passed│  │
│  │ #4 │ Google Speech v2     │ 19.4% ■ │ 6.5%         │ 3.4%         │ 9.5%         │ 27.0%   │ Passed│  │
│  │ #5 │ AssemblyAI Univ-2    │ 21.3% ■ │ 9.8%         │ 2.2%         │ 9.3%         │ 29.5%   │ Passed│  │
│  │ #6 │ Rev.ai Async API     │ 24.6% ■ │ 11.2%        │ 3.1%         │ 10.3%        │ 32.1%   │ Passed│  │
│  │ #7 │ SpeechBrain ECAPA    │ 25.9% ■ │ 8.4%         │ 5.5%         │ 12.0%        │ 34.0%   │ Passed│  │
│  │ #8 │ Kaldi / BUT VBx      │ 27.2% ■ │ 9.1%         │ 6.0%         │ 12.1%        │ 36.2%   │ Passed│  │
│  │ #9 │ AWS Transcribe v2    │ 28.5% ■ │ 14.2%        │ 3.8%         │ 10.5%        │ 37.8%   │ Passed│  │
│  │ #10│ Deepgram Nova-3      │ 67.1% ■ │ 59.4%        │ 1.2%         │ 6.5%         │ 71.2%   │ Warning│ │
│  └────┴──────────────────────┴─────────┴──────────────┴──────────────┴──────────────┴─────────┴───────┘  │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  INTERACTIVE MODEL INSPECTION DRAWER (Clicking a row expands deep diagnostic telemetry)               │
│  ┌───────────────────────────────────────────────────┬──────────────────────────────────────────────┐  │
│  │ Selected: Deepgram Nova-3                         │ Error Type Composition Breakdown             │  │
│  │ Type: Commercial Integrated ASR API               │ [ Missed Speech: 88.5% of total error      ] │  │
│  │ Pricing: $0.31 / audio hour                       │ [ Speaker Confusion: 9.7%                  ] │  │
│  │ Real-Time Factor (RTF): 0.02 (Ultra-fast batch)   │ [ False Alarm: 1.8%                        ] │  │
│  │ Overlap Detection Mode: Single-speaker serialized │ Diagnostic Finding: High energy-threshold    │  │
│  │ Total Benchmark Recordings: 240 / 240 Completed   │ VAD clips soft conversational turns.         │  │
│  └───────────────────────────────────────────────────┴──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Interactive Controls & Filtering Specifications

1. **Acoustic Domain Filters:**
   - `All Domains (Default)`: Aggregate 60-hour benchmark.
   - `In-Person Room Meetings (20 hrs)`: Multi-talker high-reverberation room scenarios.
   - `Virtual Calls (15 hrs)`: Headset, laptop mic, network VoIP packet loss artifacts.
   - `Contact Center Telephony (15 hrs)`: 8 kHz narrowband single-channel calls.
   - `Field Ambient Audio (10 hrs)`: Real-world street noise and high background chatter.

2. **Scoring Setting Toggles:**
   - **Collar Slider / Selector:** Toggle between `0.25s (Standard NIST tolerance)` and `0.00s (Strict boundary precision)`.
   - **Overlap Toggle:** Toggle between `Scored (Default)` and `Excluded (Lenient baseline)`.
   - **Speaker Count Mode:** Fixed to `Blind (k unknown)` to preserve benchmark integrity.

3. **Demographic / Regional Filters:**
   - Filter by regional Indian accent cluster (North, South, East, West, Code-Switched Hinglish).

---

## 3. Visual Components & What Sits Next to Each Score

A single headline percentage can be misleading. Beside every score in the table, our design provides four embedded contextual indicators:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                  DETAIL OF WHAT SITS NEXT TO EACH SCORE                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ 1. 95% Confidence Interval Tag:                                              │
│    14.2%  ±0.8%  [13.4% ──●── 15.0%] (Derived via 10k bootstrap resamples)   │
│                                                                              │
│ 2. Tri-Partite Error Breakdown Mini-Bar:                                     │
│    ████████░░░░░░▒▒                                                          │
│    [Blue = Miss (4.8%) | Gray = False Alarm (2.1%) | Orange = Conf (7.3%)]  │
│                                                                              │
│ 3. Operational Telemetry Badges:                                            │
│    • Real-Time Factor Badge: [⚡ RTF: 0.04x]                                 │
│    • Hardware / Cost Badge:  [💵 $0.08 / hr]                                 │
│    • Deployment Modality:    [📦 Self-Hosted Docker] or [☁️ Cloud REST API] │
│                                                                              │
│ 4. Reliability & Failure Tracker:                                            │
│    [ ✅ 240/240 Passed ] or [ ⚠️ 2 Failed / 238 Passed (OOM on 8-spk) ]       │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Model Deep-Dive Page & Interactive Waveform Inspector

When a user clicks on any model row, they are routed to the **Model Deep-Dive Page** (implemented in `frontend/src/pages/ModelDetail.jsx`), featuring:
- **Radar Chart:** 6 axes comparing Overlap Resilience, Low-Noise Purity, Telephony Robustness, Speed, Cost Efficiency, and Speaker Count Discovery accuracy.
- **Waveform Timeline Inspector:** An interactive playback component showing the ground-truth reference speaker bars aligned against the model's predicted hypothesis bars, with color-coded discrepancy highlights for Missed Speech (red), False Alarm (yellow), and Speaker Confusion (purple).

