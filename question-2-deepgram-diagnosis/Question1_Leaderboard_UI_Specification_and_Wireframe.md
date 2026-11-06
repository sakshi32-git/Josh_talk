# Leaderboard Product Specification & UI Wireframe
## Voice of India Diarization-Bench (VoI-DiarBench)

This document provides the full product design specification, user experience flow, and visual wireframe for the **Voice of India Diarization Leaderboard**.

---

## 1. Information Architecture & Key User Flows

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                   VOICE OF INDIA                                       │
│                         SPEAKER DIARIZATION LEADERBOARD                                │
│                     Measuring Speech AI Under Real Indian Conditions                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [Global Filter Bar: Use Case | Acoustic Domain | Speaker Count | Accent | License]     │
├───────────────────────────────────┬─────────────────────────────────────────────────────┤
│ PRIMARY BENCHMARK TABLE           │ DRILLDOWN INSPECTOR (Click-to-Expand)               │
│ - Rank & System Name              │ - Error Breakdown: Missed / False Alarm / Confusion │
│ - Total DER (with 95% CI)         │ - Per-Accent Performance Breakdown                  │
│ - JER & Word Diarization (cpWER)  │ - RTF (Latency) & Compute/API Cost Analysis         │
│ - Robustness Badges               │ - Audio Sample Waveform & Segment Comparison Viewer │
└───────────────────────────────────┴─────────────────────────────────────────────────────┘
```

---

## 2. Visual Wireframe Mockup

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  [LOGO] Josh Talks | Voice of India            DIARIZATION LEADERBOARD               [Docs] [Methodology] [Submit Model]│
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  🔍 Search Models...     │ Filter by: [ Domain: Telephony (8kHz) ▼ ] [ Speakers: 3-4 ▼ ] [ Accent: All India ▼ ]       │
│  [✓] Standard Collar (0.25s)   [ ] Strict Collar (0.0s)   [✓] Score Overlapping Speech   [✓] Exclude Unknown Cardinality│
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ RANK  SYSTEM NAME               PROVIDER        TYPE     DER (95% CI) ↓  JER     MS %   FA %   SC %   RTF    COST/1k HR  │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  🥇 1  pyannote.audio 3.1       Bredin / OSS    Open     11.4% ±0.8%     14.2%   4.1%   2.3%   5.0%   0.08x  $4.50 (GPU) │
│  🥈 2  NeMo Sortformer v2.0     NVIDIA          Open     12.8% ±0.9%     15.8%   4.8%   3.1%   4.9%   0.05x  $3.80 (GPU) │
│  🥉 3  Speechmatics Flow        Speechmatics    API      13.5% ±0.7%     16.1%   5.2%   2.9%   5.4%   0.12x  $18.00      │
│     4  AssemblyAI Universal-2   AssemblyAI      API      15.2% ±1.1%     18.4%   5.9%   3.8%   5.5%   0.15x  $15.00      │
│     5  Google Chirp 2 (v2 API)  Google Cloud    API      16.9% ±1.0%     20.2%   7.1%   4.2%   5.6%   0.18x  $16.00      │
│     6  Azure AI Speech          Microsoft       API      17.4% ±1.2%     21.0%   6.8%   4.9%   5.7%   0.14x  $16.50      │
│     7  ElevenLabs Scribe v2     ElevenLabs      API      19.1% ±1.4%     23.5%   8.4%   4.5%   6.2%   0.22x  $22.00      │
│     8  AWS Transcribe           Amazon          API      21.3% ±1.5%     25.8%   9.6%   5.1%   6.6%   0.20x  $14.40      │
│     9  WhisperX (PyAnnote VAD)  Open Source     Open     22.8% ±1.6%     27.1%   8.9%   7.2%   6.7%   0.28x  $6.20 (GPU) │
│    10  Deepgram Nova-3          Deepgram        API      48.6% ±2.8%*    54.2%  38.2%   4.1%   6.3%   0.04x  $7.50       │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
  * Note on Deepgram Nova-3: High DER driven by extreme Missed Speech on overlapping and noisy speech segments.
```

---

## 3. Drill-Down Model Inspector Panel (When a User Clicks a System Row)

When an engineering lead or researcher clicks on any system (e.g., **Deepgram Nova-3** or **pyannote.audio 3.1**), a detailed diagnostic panel slides open:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ◀ Back to Table  |  DEEPGRAM NOVA-3 DETAILED DIAGNOSTIC VIEW                                                            │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ OVERALL DER: 48.6%   │   JER: 54.2%   │   RTF: 0.04x (Ultra-fast)   │   PRICING: $0.0075 / audio min ($7.50 / hr)          │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ ERROR PROFILE:                                                                                                         │
│ █ Missed Speech (MS): 38.2%  ████████████████████████████████████████ (Massive voice dropout on overlap & soft audio) │
│ █ False Alarm (FA):   4.1%   ████ (Low false positive rate)                                                            │
│ █ Speaker Conf (SC):  6.3%   ██████ (Good speaker clustering when speech is detected)                                  │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ PERFORMANCE ACROSS ACOUSTIC ENVIRONMENTS:                                                                              │
│ • Telephony 8kHz (2 Speakers):           16.2% DER  [Good]                                                             │
│ • Room Mics (Shared 4 Speakers):         52.8% DER  [Poor - drops multi-speaker interruptions]                         │
│ • High Ambient Noise / Outdoor (Bilingual): 67.1% DER [Critical - drops low SNR segments]                             │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ INTERACTIVE WAVEFORM & SEGMENT VIEWER (Ground Truth vs Model Hypothesis):                                              │
│                                                                                                                        │
│ Reference: [Speaker 1: "Haan bilkul"] [Speaker 2: "Yes, exactly, I agree"] [Speaker 1: "Let's close this"]            │
│            └──────── 00:01.2 ───────┘ └──────── 00:02.0 ─────────────────┘ └──────── 00:04.5 ─────────┘               │
│                                                                                                                        │
│ Nova-3:    [Speaker 1: "Haan bilkul"] [       MISSED SPEECH GAP       ] [Speaker 1: "Let's close"]                     │
│            └──────── 00:01.2 ───────┘ └──────── 00:02.0 to 00:03.8 ───┘ └──────── 00:04.5 ─────────┘                 │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ RECOMMENDED BEST USE CASE: Fast 2-person clean telephony interviews. NOT recommended for multi-party boardroom audio. │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Key Filter Controls & Functional Specifications

1. **Acoustic Domain Selector:**
   - `All Domains`
   - `Telephony / Contact Center (8 kHz)`
   - `Shared Room Boundary Mics (In-person meetings)`
   - `Video Conferencing (Mixed VoIP audio)`
   - `Outdoor / High Noise`

2. **Speaker Cardinality Filter:**
   - `2 Speakers (Dyadic calls)`
   - `3 - 4 Speakers (Small team meetings)`
   - `5 - 8 Speakers (Boardrooms / Panels)`

3. **Linguistic / Accent Region Filter:**
   - `National Aggregate`
   - `Northern Cluster (Hindi / Hinglish / Punjabi accent)`
   - `Southern Cluster (Tamil / Telugu / Kannada / Malayalam accent)`
   - `Eastern Cluster (Bengali / Assamese accent)`
   - `Western Cluster (Marathi / Gujarati accent)`

4. **Scoring Preset Toggle:**
   - **Standard Evaluation:** Collar = 0.250s, Overlap = Scored.
   - **Zero-Tolerance / Strict:** Collar = 0.000s, Overlap = Scored.
   - **Legacy Mode (For Comparison):** Collar = 0.250s, Overlap = Ignored.

5. **Export & Transparency Tools:**
   - **Download RTTM Files:** Allows users to download all baseline and model hypothesis RTTM files.
   - **Download Scoring Script:** Provides the exact `dscore` invocation command to reproduce published numbers on local machines.
